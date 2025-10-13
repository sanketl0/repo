from os import access
from rest_framework import serializers
from .models import Company, Branch,Defaults
from registration.models import  Feature
from registration.serializers import FeatureSerializer

from item.serializers.item_serializers import ShortItemSerializer
from django.core.serializers import serialize
#This Serializers Are Used All the Company Details

class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = '__all__'
    def to_representation(self,instance):
        ret = super().to_representation(instance)
        ret['company_name'] = instance.company_id.company_name
        ret['label'] = instance.branch_name
        ret['value'] = instance.branch_id
        return ret

class BranchSerializerV1(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = '__all__'

class DefaultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Defaults
        fields = '__all__'

class CompanyGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields =  ['company_id','company_name','city','state','primary_email','financial_year','company_type']


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        exclude =  ['invoice_sequence','is_copied_coa','company_edit_id','report_basis']

    def __init__(self, *args, **kwargs):
        # Extract and remove the custom argument from kwargs
        self.user = kwargs.pop('user', None)
        # Call the parent's __init__ method with the remaining kwargs
        super(CompanySerializer, self).__init__(*args, **kwargs)
    
    def to_representation(self,instance):
        ret = super().to_representation(instance)
        obj = instance.subscribe_companies.all()[0]
        ret['paid'] = obj.get_plan_subscribe()
        ret['features'] = FeatureSerializer(Feature.objects.get(user_id=instance.user.id)).data
        ret['plan_name'] = obj.plan.name
        ret['end_date'] = obj.end_date
        ret['branches'] = []
        user = instance.user
        if self.user:
            access = self.user.user_access.all()[0]
            if access:
                branches = access.branches.filter(company_id=instance.company_id)
                print([each.branch_id for each in branches])
                branches = branches.order_by('created_date')
                ret['branches'] = BranchSerializer(branches, many=True).data
        elif user:
            access = user.user_access.all()[0]
            if access:
                branches = access.branches.order_by('created_date')
                ret['branches'] = BranchSerializer(branches,many=True).data
        return ret
    
    # def to_representation(self, instance):
        
    #     ret = super().to_representation(instance)
    #     obj = instance.subscribe_companies.all()[0]
    #     ret['paid'] = obj.get_plan_subscribe()
    #     ret['features'] = FeatureSerializer(Feature.objects.get(user_id=instance.user.id)).data
    #     ret['plan_name'] = obj.plan.name
    #     ret['end_date'] = obj.end_date

    #     # Always return company branches
    #     branches = instance.company_branches.order_by('created_date')
    #     ret['branches'] = BranchSerializer(branches, many=True).data

    #     return ret
class CompanySerializerUpdate(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        # Extract and remove the custom argument from kwargs
        self.user = kwargs.pop('user', None)
        # Call the parent's __init__ method with the remaining kwargs
        super(CompanySerializerUpdate, self).__init__(*args, **kwargs)

    class Meta:
        model = Company
        exclude =  ['invoice_sequence','is_copied_coa','is_new_company','company_edit_id','report_basis','logo_image']

    def to_representation(self,instance):
        ret = super().to_representation(instance)
        obj = instance.subscribe_companies.all()[0]
        ret['paid'] = obj.get_plan_subscribe()
        ret['features'] = FeatureSerializer(Feature.objects.get(user_id=instance.user.id)).data
        ret['plan_name'] = obj.plan.name
        ret['end_date'] = obj.end_date
        ret['logo_image'] = instance.get_logo_url()
        ret['branches'] = []
        user = instance.user
        if self.user:
            access = self.user.user_access.all()[0]
            if access:
                branches = access.branches.filter(company_id=instance.company_id)
                print([each.branch_id for each in branches])
                branches = branches.order_by('created_date')
                ret['branches'] = BranchSerializer(branches, many=True).data
        elif user:
            access = user.user_access.all()[0]
            if access:
                branches = access.branches.order_by('created_date')
                ret['branches'] = BranchSerializer(branches, many=True).data
        return ret

class AllCompanyNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['company_id', 'company_name','state','financial_year','user','logo_image']


        #depth=1

class ShortBranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = ['branch_id','company_id','branch_name','gstin','transaction_series','address']
        depth=1
        
        
# class CompanySerializer(serializers.ModelSerializer): 
#     #company_items=ShortItemSerializer(many=True) #Nested Serilizations
#     class Meta:
#         model = Company
#         fields = ['company_id','company_name','company_items']
        
