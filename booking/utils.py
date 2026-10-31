from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

def enviar_correos_confirmacion(booking_data, referencia):
    cliente_email = booking_data.get('mail')
    cliente_nombre = f"{booking_data.get('name')} {booking_data.get('lastname')}"
    total_formateado = f"{int(booking_data.get('total', 0)):,}"

    contexto = {
        'referencia': referencia,
        'cliente_nombre': cliente_nombre,
        'cliente_email': cliente_email,
        'telefono': booking_data.get('phone'),
        'servicio': booking_data.get('tour'),
        'fecha': booking_data.get('checkin'),
        'hotel_origen': booking_data.get('hotel'),
        'total_cop': total_formateado,
    }

    # 1. Cargar y enviar correo al Cliente
    html_cliente = render_to_string('emails/email_cliente.html', contexto)
    msg_cliente = EmailMultiAlternatives(
        subject=f"¡Reserva Confirmada #{referencia}! - Transturismo Cartagena",
        body=f"Hola {cliente_nombre}, tu reserva #{referencia} para {booking_data.get('tour')} ha sido confirmada.",
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[cliente_email]
    )
    msg_cliente.attach_alternative(html_cliente, "text/html")
    msg_cliente.send(fail_silently=False)

    # 2. Cargar y enviar correo al Administrador
    html_admin = render_to_string('emails/email_admin.html', contexto)
    msg_admin = EmailMultiAlternatives(
        subject=f"🚨 NUEVA RESERVA PAGADA #{referencia} - {cliente_nombre}",
        body=f"Nueva reserva #{referencia} de {cliente_nombre}.",
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[getattr(settings, 'ADMIN_EMAIL', settings.EMAIL_HOST_USER)]
    )
    msg_admin.attach_alternative(html_admin, "text/html")
    msg_admin.send(fail_silently=False)