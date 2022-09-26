from .models import Pergunta
from datetime import datetime, timedelta
data = datetime.today()-timedelta(days=7)
Pergunta.objects.order_by('-data').filter(data__lte=data,publicada=False).update(publicada=True)