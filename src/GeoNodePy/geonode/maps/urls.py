from django.conf.urls.defaults import patterns, url

js_info_dict = {
    'packages': ('geonode.maps',),
}

urlpatterns = patterns('geonode.maps.views',
    (r'^$', 'maps'),
    url(r'^new$', 'newmap', name="map_new"),
    url(r'^new/data$', 'newmapJSON'),
    (r'^(?P<mapid>\d+)$', 'map_controller'),
    (r'^(?P<mapid>\d+)/view$', 'view'),
    (r'^(?P<mapid>\d+)/download/$', 'map_download'),
    (r'^check/$', 'check_download'),
    (r'^embed/$', 'embed'),
    (r'^(?P<mapid>\d+)/embed$', 'embed'),
    (r'^(?P<mapid>\d+)/data$', 'mapJSON'),
    url(r'^search/?$', 'maps_search_page', name='maps_search'),
    url(r'^search/api/?$', 'maps_search', name='maps_search_api'),
    url(r'^(?P<mapid>\d+)/ajax-permissions$', 'ajax_map_permissions', name='ajax_map_permissions'),
    url(r'^change-poc/(?P<ids>\w+)$', 'change_poc', name="change_poc"),
)

datapatterns = patterns('geonode.maps.views',
  url(r'^$', 'browse_data', name='data'),
  url(r'^acls/?$', 'layer_acls', name='layer_acls'),
  url(r'^search/?$', 'search_page', name='old_search'),
  url(r'^search/api/?$', 'metadata_search', name='old_search_api'),
  url(r'^search/detail/?$', 'search_result_detail', name='search_result_detail'),
  url(r'^api/batch_permissions/?$', 'batch_permissions'),
  url(r'^api/batch_delete/?$', 'batch_delete'),
  url(r'^upload$', 'upload_layer', name='data_upload'),
  (r'^download$', 'batch_layer_download'),
  url(r'^(?P<layername>[^/]*)$', 'layer_detail', name="layer_detail"),
  url(r'^(?P<layername>[^/]*)/metadata$', 'layer_metadata', name="layer_metadata"),
  url(r'^(?P<layername>[^/]*)/remove$', 'layer_remove', name="layer_remove"),
  url(r'^(?P<layername>[^/]*)/replace$', 'layer_replace', name="layer_replace"),
  url(r'^(?P<layername>[^/]*)/style$', 'layer_style', name="layer_style"),
  (r'^(?P<layername>[^/]*)/ajax-permissions$', 'ajax_layer_permissions'),
)

servicepatterns = patterns('geonode.maps.views',
    url(r'^$', 'services', name='services'),
    url(r'^register/$', 'register_service', name="register_service"),
    url(r'^register_layers/$', 'register_layers', name="register_layers"),
    url(r'^(?P<service_id>\d+)/$', 'service_detail', name='service_detail'),
    url(r'^(?P<service_id>\d+)/edit$', 'edit_service', name='edit_service'),
    url(r'^(?P<service_id>\d+)/remove', 'remove_service', name='remove_service'),
    url(r'^(?P<service_id>\d+)/ajax-permissions$', 'ajax_service_permissions', name='ajax_service_permissions'),
    url(r'^(?P<service_id>\d+)/layers$', 'service_layers', name='service_layers'),
)

collectionpatterns = patterns('geonode.maps.views',
    url(r'^$', 'collections', name="collections"),
    url(r'^(?P<slug>[^/]*)$', 'collection_detail', name="collection_detail"),
    url(r'^(?P<slug>(?:[-\w]+/)*[-\w]+)/edit$', 'collection_edit', name="collection_edit"),
    url(r'^(?P<slug>(?:[-\w]+/)*[-\w]+)/remove$', 'collection_remove', name="collection_remove"),
    url(r'^(?P<slug>(?:[-\w]+/)*[-\w]+)/download$', 'collection_download', name="collection_download"),
    url(r'^(?P<slug>(?:[-\w]+/)*[-\w]+)/permissions$', 'collection_ajax_permissions', name="collection_ajax_permissions"),
)
