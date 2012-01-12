from django.http import Http404, HttpResponseForbidden
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.views.decorators.http import require_POST

from django.contrib.auth.decorators import login_required

from geonode.groups.forms import GroupInviteForm, GroupForm, GroupUpdateForm
from geonode.groups.models import Group, GroupInvitation


def group_list(request):
    ctx = {
        "object_list": Group.objects.all(),
    }
    ctx = RequestContext(request, ctx)
    return render_to_response("groups/group_list.html", ctx)


@login_required
def group_create(request):
    if request.method == "POST":
        form = GroupForm(request.POST, request.FILES)
        if form.is_valid():
            group = form.save(commit=False)
            group.save()
            group.join(request.user, role="manager")
            return redirect("group_detail", group.slug)
    else:
        form = GroupForm()
    
    return render_to_response("groups/group_create.html", {
        "form": form,
    }, context_instance=RequestContext(request))


@login_required
def group_update(request, slug):
    group = Group.objects.get(slug=slug)
    if not group.user_is_role(request.user, role="manager"):
        return HttpResponseForbidden()
    
    if request.method == "POST":
        form = GroupUpdateForm(request.POST, request.FILES, instance=group)
        if form.is_valid():
            group = form.save(commit=False)
            group.save()
            return redirect("group_detail", group.slug)
    else:
        form = GroupForm(instance=group)
    
    return render_to_response("groups/group_update.html", {
        "form": form,
    }, context_instance=RequestContext(request))


def group_detail(request, slug):
    group = get_object_or_404(Group, slug=slug)
    
    if not group.can_view(request.user):
        raise Http404()
    
    ctx = {
        "object": group,
        "maps": [], # @@@
        "members": group.member_queryset(),
        "is_member": group.user_is_member(request.user),
    }
    ctx = RequestContext(request, ctx)
    return render_to_response("groups/group_detail.html", ctx)


def group_members(request, slug):
    group = get_object_or_404(Group, slug=slug)
    ctx = {}
    
    if not group.can_view(request.user):
        raise Http404()
    
    if group.access in ["public-invite", "private"] and group.user_is_role(request.user, "manager"):
        ctx["invite_form"] = GroupInviteForm()
    
    ctx.update({
        "object": group,
        "members": group.member_queryset(),
        "is_member": group.user_is_member(request.user),
        "is_manager": group.user_is_role(request.user, "manager"),
    })
    ctx = RequestContext(request, ctx)
    return render_to_response("groups/group_members.html", ctx)


@require_POST
def group_invite(request, slug):
    group = get_object_or_404(Group, slug=slug)
    
    if not group.can_invite(request.user):
        raise Http404()
    
    form = GroupInviteForm(request.POST)
    
    if form.is_valid():
        for user in form.cleaned_data["users"]:
            group.invite(user, request.user, role=form.cleaned_data["role"])
    
    return redirect("group_members", slug=group.slug)


@login_required
def group_invite_response(request, token):
    invite = get_object_or_404(GroupInvitation, token=token)
    
    if request.method == "POST":
        if "accept" in request.POST:
            invite.accept(request.user)
        
        if "decline" in request.POST:
            invite.decline()
        
        return redirect("group_detail", slug=invite.group.slug)
    else:
        return render_to_response("groups/group_invite_response.html")
