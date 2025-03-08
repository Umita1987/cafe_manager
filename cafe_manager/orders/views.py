from django.db.models import Q, Sum
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.forms import BaseInlineFormSet

from .forms import OrderItemFormSet, OrderForm
from .models import Order

# 🌟 Список заказов (поиск + фильтрация)
class OrderListView(ListView):
    """Отображает список заказов с возможностью поиска и фильтрации по статусу."""
    model = Order
    template_name = 'orders/order_list.html'
    context_object_name = 'orders'

    def get_queryset(self) -> list[Order]:
        """Фильтрует заказы по номеру стола или статусу."""
        queryset = super().get_queryset()
        query: str | None = self.request.GET.get('q')
        status_filter: str | None = self.request.GET.get('status')

        if query:
            queryset = queryset.filter(Q(table_number__icontains=query))

        if status_filter:
            queryset = queryset.filter(status=status_filter)

        return queryset


# 🌟 Создание заказа
class OrderCreateView(CreateView):
    """Создание нового заказа с добавлением блюд."""
    model = Order
    form_class = OrderForm
    template_name = 'orders/order_form.html'

    def get_context_data(self, **kwargs) -> dict:
        """Добавляет форму для блюд в контекст шаблона."""
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['items']: BaseInlineFormSet = OrderItemFormSet(self.request.POST)
        else:
            data['items']: BaseInlineFormSet = OrderItemFormSet()
        return data

    def form_valid(self, form: OrderForm) -> HttpResponseRedirect:
        """Сохраняет заказ и пересчитывает его стоимость."""
        context = self.get_context_data()
        items: BaseInlineFormSet = context['items']
        self.object: Order = form.save()

        if items.is_valid():
            items.instance = self.object
            items.save()
            self.object.calculate_total()  # Пересчитываем сумму заказа
        return redirect('order_list')


# 🌟 Удаление заказа
class OrderDeleteView(DeleteView):
    """Удаление заказа по ID."""
    model = Order
    template_name = 'orders/order_confirm_delete.html'
    success_url = reverse_lazy('order_list')


# 🌟 Редактирование заказа (номер стола, блюда, статус)
class OrderUpdateView(UpdateView):
    """Редактирование существующего заказа."""
    model = Order
    form_class = OrderForm
    template_name = 'orders/order_form.html'
    success_url = reverse_lazy('order_list')

    def get_context_data(self, **kwargs) -> dict:
        """Добавляет форму для блюд в контекст шаблона."""
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['items']: BaseInlineFormSet = OrderItemFormSet(self.request.POST, instance=self.object)
        else:
            context['items']: BaseInlineFormSet = OrderItemFormSet(instance=self.object)
        return context

    def form_valid(self, form: OrderForm) -> HttpResponseRedirect:
        """Сохраняет изменения в заказе и пересчитывает его стоимость."""
        context = self.get_context_data()
        items_formset: BaseInlineFormSet = context['items']

        if items_formset.is_valid():
            self.object: Order = form.save()
            items_formset.instance = self.object
            items_formset.save()
            self.object.calculate_total()  # Пересчет суммы заказа
            return super().form_valid(form)

        return self.render_to_response(self.get_context_data(form=form))


# 🌟 Страница с расчетом выручки за смену
class RevenueView(TemplateView):
    """Отображает выручку за смену (заказы со статусом "оплачено")."""
    template_name = 'orders/revenue.html'

    def get_context_data(self, **kwargs) -> dict:
        """Подсчитывает сумму всех оплаченных заказов."""
        context = super().get_context_data(**kwargs)
        total_revenue: int | float = Order.objects.filter(status='paid').aggregate(total=Sum('total_price'))['total'] or 0
        context['total_revenue'] = total_revenue
        return context
