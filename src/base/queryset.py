from django.forms import model_to_dict


def to_list(queryset):
    return list(map(model_to_dict, queryset))