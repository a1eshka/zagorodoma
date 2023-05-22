from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth import get_user_model
from requests import request
from posts_project.settings import DEFAULT_FROM_EMAIL, EMAIL_HOST_PASSWORD, EMAIL_HOST_USER
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import ssl
User = get_user_model()

def send_activate_email_message(user_id):
    """
    Функция отправки письма с подтверждением для аккаунта
    """
    user = get_object_or_404(User, id=user_id)
    current_site = '127.0.0.1'
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    activation_url = reverse_lazy('confirm_email', kwargs={'uidb64': uid, 'token': token})
    current_site = 'http://127.0.0.1:8000'
    html = '''Пожалуйста, перейдите по следующей ссылке, чтобы подтвердить свой адрес электронной почты: <a href="{}{}">{}{}"></a>'''.format(current_site, activation_url, current_site, activation_url)
    email_from = EMAIL_HOST_USER
    password = EMAIL_HOST_PASSWORD
    email_to = user.email
    email_message = MIMEMultipart()
    email_message['From'] = DEFAULT_FROM_EMAIL
    email_message['To'] = email_to
    email_message['Subject'] = f'Подтверждение электронного адреса.'
# Attach the html doc defined earlier, as a MIMEText html content type to the MIME message
    email_message.attach(MIMEText(html, "html"))
    email_string = email_message.as_string()
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.mail.ru", 465, context=context) as server:
        server.login(email_from, password)
        server.sendmail(email_from, email_to, email_string)
    return redirect('/')


def send_publish_post_message(author,post_url):
    
    html = '''
<html>
<body>
<table class="es-wrapper" width="100%" cellspacing="0" cellpadding="0" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;padding:0;Margin:0;width:100%;height:100%;background-repeat:repeat;background-position:center top;background-color:#FFFFFF">
<tr>
<td valign="top" style="padding:0;Margin:0">
<table cellpadding="0" cellspacing="0" class="es-content" align="center" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;table-layout:fixed !important;width:100%">
<tr>
<td align="center" style="padding:0;Margin:0">
<table bgcolor="#efefef" class="es-content-body" align="center" cellpadding="0" cellspacing="0" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;background-color:#EFEFEF;border-radius:20px 20px 0 0;width:600px">
<tr>
<td align="left" style="padding:0;Margin:0;padding-top:40px;padding-left:40px;padding-right:40px">
<table cellpadding="0" cellspacing="0" width="100%" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
<tr>
<td align="center" valign="top" style="padding:0;Margin:0;width:520px">
<table cellpadding="0" cellspacing="0" width="100%" role="presentation" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
<tr>
<td align="left" style="padding:0;Margin:0;font-size:0px"><a target="_blank" href="" style="-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;text-decoration:underline;color:#2D3142;font-size:18px"><img src="https://gtbyhc.stripocdn.email/content/guids/CABINET_ee77850a5a9f3068d9355050e69c76d26d58c3ea2927fa145f0d7a894e624758/images/group_4076323.png" alt="Confirm email" style="display:block;border:0;outline:none;text-decoration:none;-ms-interpolation-mode:bicubic;border-radius:100px" width="100" title="Confirm email"></a></td>
</tr>
</table></td>
</tr>
</table></td>
</tr>
<tr>
<td align="left" style="padding:0;Margin:0;padding-top:20px;padding-left:40px;padding-right:40px">
<table cellpadding="0" cellspacing="0" width="100%" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
<tr>
<td align="center" valign="top" style="padding:0;Margin:0;width:520px">
<table cellpadding="0" cellspacing="0" width="100%" bgcolor="#fafafa" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:separate;border-spacing:0px;background-color:#fafafa;border-radius:10px" role="presentation">
<tr>
<td align="left" style="padding:20px;Margin:0"><h3 style="Margin:0;line-height:34px;mso-line-height-rule:exactly;font-family:Imprima, Arial, sans-serif;font-size:28px;font-style:normal;font-weight:bold;color:#2D3142">Поздравляем!</h3><p style="Margin:0;-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;font-family:Imprima, Arial, sans-serif;line-height:27px;color:#2D3142;font-size:18px"><br></p><p style="Margin:0;-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;font-family:Imprima, Arial, sans-serif;line-height:27px;color:#2D3142;font-size:18px">Ваше объявление было успешно опубликовано на нашем сайте.<br>Объявление доступно по ссылке: {}&nbsp;<br></p></td>
</tr>
</table></td>
</tr>
</table></td>
</tr>
</table></td>
</tr>
</table>
<table cellpadding="0" cellspacing="0" class="es-content" align="center" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;table-layout:fixed !important;width:100%">
<tr>
<td align="center" style="padding:0;Margin:0">
<table bgcolor="#efefef" class="es-content-body" align="center" cellpadding="0" cellspacing="0" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;background-color:#EFEFEF;width:600px">
<tr>
<td align="left"
style="Margin:0;padding-top:30px;padding-bottom:40px;padding-left:40px;padding-right:40px">
<table cellpadding="0" cellspacing="0" width="100%" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
<tr>
<td align="center" valign="top" style="padding:0;Margin:0;width:520px">
<table cellpadding="0" cellspacing="0" width="100%" role="presentation" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
<tr>
<td align="center" style="padding:0;Margin:0"><!--[if mso]><a href="" target="_blank" hidden>
<v:roundrect xmlns:v="urn:schemas-microsoft-com:vml" xmlns:w="urn:schemas-microsoft-com:office:word" esdevVmlButton href=""
style="height:56px; v-text-anchor:middle; width:520px" arcsize="50%" stroke="f" fillcolor="#7630f3">
<w:anchorlock></w:anchorlock>
<center style='color:#ffffff; font-family:Imprima, Arial, sans-serif; font-size:22px; font-weight:700; line-height:22px; mso-text-raise:1px'>Перейти к объявлению</center>
</v:roundrect></a>
<![endif]--><!--[if !mso]><!— —><span class="msohide es-button-border" style="border-style:solid;border-color:#2CB543;background:#7630f3;border-width:0px;display:block;border-radius:30px;width:auto;mso-border-alt:10px;mso-hide:all"><a href="{}" class="es-button msohide" target="_blank" style="mso-style-priority:100 !important;text-decoration:none;-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;color:#FFFFFF;font-size:22px;padding:15px 20px 15px 20px;display:block;background:#7630f3;border-radius:30px;font-family:Imprima, Arial, sans-serif;font-weight:bold;font-style:normal;line-height:26px;width:auto;text-align:center;mso-hide:all;padding-left:5px;padding-right:5px;border-color:#7630f3">Перейти к объявлению</a></span><!--<![endif]--></td>
</tr>
</table></td>
</tr>
</table></td>
</tr>
<tr>
<td align="left" style="padding:0;Margin:0;padding-left:40px;padding-right:40px">
<table cellpadding="0" cellspacing="0" width="100%" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
<tr>
<td align="center" valign="top" style="padding:0;Margin:0;width:520px">
<table cellpadding="0" cellspacing="0" width="100%" role="presentation" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
<tr>
<td align="left" style="padding:0;Margin:0"><p style="Margin:0;-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;font-family:-apple-system, blinkmacsystemfont, 'segoe ui', roboto, helvetica, arial, sans-serif, 'apple color emoji', 'segoe ui emoji', 'segoe ui symbol';line-height:27px;color:#2D3142;font-size:18px">С Уважением,<br>Команда Zagorodoma.</p></td>
</tr>
<tr>
<td align="center" style="padding:0;Margin:0;padding-bottom:20px;padding-top:40px;font-size:0">
<table border="0" width="100%" height="100%" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
<tr>
<td style="padding:0;Margin:0;border-bottom:1px solid #666666;background:unset;height:1px;width:100%;margin:0px"></td>
</tr>
</table></td>
</tr>
<tr>
<td align="center" style="padding:0;Margin:0;padding-top:10px;padding-bottom:10px;font-size:0px"><a target="_blank" href="https://zagorodoma.ru" style="-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;text-decoration:underline;color:#2D3142;font-size:18px"><img class="adapt-img" src="http://cdn.zagorodoma.ru/media/static/logo-v2.png" alt="zagorodoma.ru" width="29%" style="display:block;border:0;outline:none;text-decoration:none;-ms-interpolation-mode:bicubic" title="zagorodoma.ru"></a></td>
</tr>
</table></td>
</tr>
</table></td>
</tr>
</table></td>
</tr>
</table></td>
</tr>
</table>
</body>
</html>
'''.format(post_url, post_url, post_url)
    email_from = EMAIL_HOST_USER
    password = EMAIL_HOST_PASSWORD
    email_to = author
    email_message = MIMEMultipart()
    email_message['From'] = DEFAULT_FROM_EMAIL
    email_message['To'] = email_to
    email_message['Subject'] = f'Ваше объявление успешно опубликовано.'
# Attach the html doc defined earlier, as a MIMEText html content type to the MIME message
    email_message.attach(MIMEText(html, "html"))
    email_string = email_message.as_string()
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.mail.ru", 465, context=context) as server:
        server.login(email_from, password)
        server.sendmail(email_from, email_to, email_string)
    