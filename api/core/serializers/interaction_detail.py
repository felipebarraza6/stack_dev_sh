from rest_framework import serializers
from api.core.models import InteractionDetail, ProfileDataConfigCatchment
from django.db.models import Sum

class InteractionDetailModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = InteractionDetail
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        catchment_point = instance.catchment_point
        total_d6 = ProfileDataConfigCatchment.objects.filter(point_catchment=catchment_point).aggregate(total=Sum('d6'))['total'] or 0
    
        # Ensure that representation['total'] is not None
        current_total = representation.get('total', 0)
        if current_total is None:
            current_total = 0
        
        representation['total'] = int(total_d6) + int(current_total)
        return representation
     
    


class InteractionDetailModelSerializerNoProcessing(serializers.ModelSerializer):
    class Meta:
        model = InteractionDetail
        fields = '__all__'