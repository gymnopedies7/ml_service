from django.db import models

# Create your models here.


class Endpoint(models.Model):
    '''
    The Endpoint object 는 ML API endpoint 를 말함
    Attributes : 
        name : endpoint 의 name으로 API URL로 사용됨
        owner : owner이름 string
        created_at : endpoint 만들어진 날짜
    '''
    name = models.CharField(max_length=128)
    owner = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)

class MLAlgorithm(models.Model):
    '''
    The MLalgorithm 은 머신러닝 알고리즘 object를 말함
    Attributes:
        name : algorithm의 이름
        description : 알고리즘 동작방법 요약
        code : 알고리즘 코드
        version : 알고리즘 버전
        owner : owner 이름
        created_at : 추가된 날짜
        parent_endpoint : the reference to the Endpoint
    '''
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=1000)
    code = models.TextField()
    version = models.CharField(max_length=128)
    owner = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    parent_endpoint = models.ForeignKey(Endpoint, on_delete=models.CASCADE)


class MLAlgorithmStatus(models.Model):
    '''
    The MLAlgorithmsStatus는 MLAlgorithms 가 변화할 수 있는 상태를 말함
    attributes:
        status: The status of algorithm in the endpoint. Can be: testing, staging, production, ab_testing.
        active: The boolean flag which point to currently active status.
        created_by: The name of creator.
        created_at: The date of status creation.
        parent_mlalgorithm: The reference to corresponding MLAlgorithm.
    '''
    status = models.CharField(max_length=128)
    active = models.BooleanField()
    created_by = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    parent_mlalgorithm = models.ForeignKey(MLAlgorithm, on_delete=models.CASCADE, related_name="status")

class MLRequest(models.Model):
    '''
    The MLRequest will keep information about all requests to ML algorithms.

    Attributes:
        input_data: The input data to ML algorithm in JSON format.
        full_response: The response of the ML algorithm.
        response: The response of the ML algorithm in JSON format.
        feedback: The feedback about the response in JSON format.
        created_at: The date when request was created.
        parent_mlalgorithm: The reference to MLAlgorithm used to compute response.
    '''
    input_data = models.TextField()
    full_response = models.TextField()
    response = models.TextField()
    feedback = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    parent_mlalgorithm = models.ForeignKey(MLAlgorithm, on_delete=models.CASCADE)


class ABTest(models.Model):
    '''
    The ABTest will keep information about A/B tests.
    Attributes:
        title: The title of test.
        created_by: The name of creator.
        created_at: The date of test creation.
        ended_at: The date of test stop.
        summary: The description with test summary, created at test stop.
        parent_mlalgorithm_1: The reference to the first corresponding MLAlgorithm.
        parent_mlalgorithm_2: The reference to the second corresponding MLAlgorithm.
    '''
    title = models.CharField(max_length = 128)
    created_by = models.CharField(max_length= 128)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    ended_at = models.DateTimeField(blank=True, null=True)
    summary = models.TextField(blank=True, null=True)

    parent_mlalgorithm_1 = models.ForeignKey(MLAlgorithm, on_delete=models.CASCADE, related_name="parent_mlalgorithm_1")
    parent_mlalgorithm_2 = models.ForeignKey(MLAlgorithm, on_delete=models.CASCADE, related_name="parent_mlalgorithm_2")

