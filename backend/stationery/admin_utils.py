from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from . models import ActiveOrders, PastOrders, ActivePrintOuts, PastPrintOuts

from django.utils import timezone
from datetime import timedelta, datetime
import calendar


# For marking an active order as completed (past)
# @staff_member_required ensures only Django admin users can access this
@staff_member_required
def delete_active_order(request, order_id):
    
    active_order = ActiveOrders.objects.get(order_id=order_id)

    new_past_order = PastOrders(order_id=order_id, user=active_order.user, item=active_order.item,
                                quantity=active_order.quantity, cost=active_order.cost,
                                custom_message=active_order.custom_message, order_time=active_order.order_time)

    new_past_order.save()
    active_order.delete()
    
    return redirect('/admin/stationery/activeorders/')

# For marking an active printout as completed (past)
@staff_member_required
def delete_active_printout(request, order_id):
    
    active_printout = ActivePrintOuts.objects.get(order_id=order_id)

    new_past_printout = PastPrintOuts(order_id=order_id, user=active_printout.user, coloured_pages=active_printout.coloured_pages,
                                black_and_white_pages=active_printout.black_and_white_pages, cost=active_printout.cost,
                                custom_message=active_printout.custom_message, order_time=active_printout.order_time,
                                file=active_printout.file)

    new_past_printout.save()
    active_printout.delete()
    
    return redirect('/admin/stationery/activeprintouts/')


# For daily, weekly and monthly orders report
@staff_member_required
def generate_order_report(request, duration):
    today = timezone.now().date()

    if duration == 'daily':
        start_date = today
        end_date = today
        report_type = 'DAILY REPORT'
    elif duration == 'weekly':
        start_date = today - timedelta(days=today.weekday())
        end_date = start_date + timedelta(days=6)
        report_type = 'WEEKLY REPORT'
    elif duration == 'monthly':
        start_date = today.replace(day=1)
        end_date = start_date.replace(day=calendar.monthrange(start_date.year, start_date.month)[1])
        report_type = 'MONTHLY REPORT'
    else:
        return redirect('/admin/')

    # gte means greater than or equal to
    all_records = PastOrders.objects.filter(order_time__gte=start_date)

    context = {
        'all_records': all_records,
        'report_type': report_type,
        'start_date': start_date,
        'end_date': end_date,
    }
    
    return render(request, 'stationery/orders/report-pdfs.html', context)

# For custom dates orders report
@staff_member_required
def generate_custom_order_report(request):
    
    if request.method == 'POST':
        
        start_date_time_str = request.POST.get('start_date_time')
        end_date_time_str = request.POST.get('end_date_time')

        # Convert string representations to datetime objects
        start_date_time_naive = datetime.strptime(start_date_time_str, '%Y-%m-%dT%H:%M')
        end_date_time_naive = datetime.strptime(end_date_time_str, '%Y-%m-%dT%H:%M')
        
        # Make datetime objects aware of the time zone (assuming your server's time zone)
        # To avoid these kinds of warnings : "received a naive datetime while time zone support is active."
        server_timezone = timezone.get_default_timezone()
        start_date_time = timezone.make_aware(start_date_time_naive, timezone=server_timezone)
        end_date_time = timezone.make_aware(end_date_time_naive, timezone=server_timezone)

        all_records = PastOrders.objects.filter(order_time__gte=start_date_time, order_time__lte=end_date_time)
        
        context = {
            'all_records': all_records,
            'report_type': 'CUSTOM REPORT',
            'start_date': start_date_time,
            'end_date': end_date_time,
        }
        
        return render(request, 'stationery/orders/report-pdfs.html', context)
    # GET REQUEST
    else:
        return render(request, 'stationery/orders/custom_report.html')
        

# For daily, weekly and monthly printouts report
@staff_member_required
def generate_printout_report(request, duration):
    today = timezone.now().date()

    if duration == 'daily':
        start_date = today
        end_date = today
        report_type = 'DAILY REPORT'
    elif duration == 'weekly':
        start_date = today - timedelta(days=today.weekday())
        end_date = start_date + timedelta(days=6)
        report_type = 'WEEKLY REPORT'
    elif duration == 'monthly':
        start_date = today.replace(day=1)
        end_date = start_date.replace(day=calendar.monthrange(start_date.year, start_date.month)[1])
        report_type = 'MONTHLY REPORT'
    else:
        return redirect('/admin/')

    # gte means greater than or equal to
    all_records = PastPrintOuts.objects.filter(order_time__gte=start_date)

    context = {
        'all_records': all_records,
        'report_type': report_type,
        'start_date': start_date,
        'end_date': end_date,
    }
    
    return render(request, 'stationery/printouts/report-pdfs.html', context)

# For custom dates printouts report
@staff_member_required
def generate_custom_printout_report(request):
    
    if request.method == 'POST':
        
        start_date_time_str = request.POST.get('start_date_time')
        end_date_time_str = request.POST.get('end_date_time')

        # Convert string representations to datetime objects
        start_date_time_naive = datetime.strptime(start_date_time_str, '%Y-%m-%dT%H:%M')
        end_date_time_naive = datetime.strptime(end_date_time_str, '%Y-%m-%dT%H:%M')
        
        # Make datetime objects aware of the time zone (assuming your server's time zone)
        # To avoid these kinds of warnings : "received a naive datetime while time zone support is active."
        server_timezone = timezone.get_default_timezone()
        start_date_time = timezone.make_aware(start_date_time_naive, timezone=server_timezone)
        end_date_time = timezone.make_aware(end_date_time_naive, timezone=server_timezone)

        all_records = PastPrintOuts.objects.filter(order_time__gte=start_date_time, order_time__lte=end_date_time)
        
        context = {
            'all_records': all_records,
            'report_type': 'CUSTOM REPORT',
            'start_date': start_date_time,
            'end_date': end_date_time,
        }
        
        return render(request, 'stationery/printouts/report-pdfs.html', context)
    # GET REQUEST
    else:
        return render(request, 'stationery/printouts/custom_report.html')
        
