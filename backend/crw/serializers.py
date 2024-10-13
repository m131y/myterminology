from rest_framework.serializers import ModelSerializer
from .models import Search_list
from .models import dict

class SearchDataSerializer(ModelSerializer):
    class Meta:
        model = Search_list
        fields = '__all__'


class dictDataSerializer(ModelSerializer):
    class Meta:
        model = dict
        fields = '__all__'