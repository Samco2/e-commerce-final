from .models import Cart
import uuid
from django.conf import settings



class Basket():
    """
    A base Basket class, providing some default behaviors that
    can be inherited or overrided, as necessary.
    """
    def __init__(self, request):
        self.session = request.session
        try:
            cart = Cart.objects.get(session_id = request.session['nonuser'], completed=False)
        except:
            request.session['nonuser'] = str(uuid.uuid4())
            cart = Cart.objects.create(session_id = request.session['nonuser'], completed=False)
        self.cart = cart

    def clear(self):
        # Remove basket from session
        del self.session['nonuser']
        self.save()


    def save(self):
        self.session.modified = True


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
