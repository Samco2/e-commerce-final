from .models import Cart
import uuid
from .basket import Basket


def basket(request):
    return {'basket': Basket(request)}



def cart_renderer(request):
   #Creating Session for non-user or user yet to be unthenticated

      try:
         cart = Cart.objects.get(session_id = request.session['nonuser'], completed=False)
      except:
         request.session['nonuser'] = str(uuid.uuid4())
         cart = Cart.objects.create(session_id = request.session['nonuser'], completed=False)

      return {
         'cart': cart
      }
