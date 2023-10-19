import sys
from .models import transport_owners_info, transport_info
from django.forms import ModelForm, forms
from django.forms.widgets import RadioSelect, Select


class transport_owners_form(ModelForm):
     class Meta:
        model = transport_owners_info
        fields = ['owner_name', 'owner_gender', 'passport', 'birth_date', 'citizenship']
        widgets = {
            'owner_gender': RadioSelect()
        }


class transport_info_form(ModelForm):
    class Meta:
        model = transport_info
        fields = ['type_id', 'transport_number',
                  # 'prev_owner_id',
                  'manufacture_date', 'cur_license_expires', 'made_in_country']
        widgets = {
            'type_id': Select(attrs={'onchange': "change_background(this);", 'id': 'type_id_select'})
        }
