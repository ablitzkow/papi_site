from perguntas.models import Pergunta
from datetime import datetime, timedelta
data = datetime.today()-timedelta(days=7)
perguntas = Pergunta.objects.order_by('-data').filter(data__lte=data,publicada=True).update(publicada=True)