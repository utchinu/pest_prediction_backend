from rest_framework import serializers 
from tutorials.models import Tutorial
 
 
class TutorialSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = Tutorial
        fields = ('id',
                  'date',
                  'crop',
                  'pest',
                  'state_name',
                  'district_name',
                  'lattitude',
                  'longitude',
                  'count')