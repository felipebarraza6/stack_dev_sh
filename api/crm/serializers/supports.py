from rest_framework import serializers

# Models
from api.crm.models import SupportSection, TicketSupport, AnswerTicket 
from .users import UserModelSerializer


class SupportSectionModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupportSection
        fields = '__all__'

class AnswerTicketModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerTicket
        fields = '__all__'

class AnswerTicketModelSerializerRetrieve(serializers.ModelSerializer):
    administrator = UserModelSerializer()
    class Meta:
        model = AnswerTicket
        fields = '__all__'

class TicketSupportModelSerializerRetrieve(serializers.ModelSerializer):
    answers = serializers.SerializerMethodField('get_answers')

    def get_answers(self, ticket):
            qs = AnswerTicket.objects.filter(ticket_support=ticket.id).order_by('created')
            serializer = AnswerTicketModelSerializerRetrieve(instance=qs, many=True)
            data = serializer.data
            return data

    class Meta:
        model = TicketSupport
        fields = '__all__'

class TicketSupportModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketSupport
        fields = '__all__'


