# Google-DDNS
Python based Google DDNS update client for GoogleDomains

Google is offering domain & DNS (https://domains.google.com/registrar) services and includes some cool features.

You can generate custom domain email & just have it forward to your gmail account. You can also set up to reply back from that address (https://support.google.com/domains/answer/3251241?hl=en)

The service also includes DDNS for your subdomain. You can set this up quickly if you have DDclient (https://support.google.com/domains/answer/6147083?hl=en) but I used this as an excuse to sit down and really dig into learning Python.

This still needs lots of work but it is functional for now. Just run it manually & check your error prints in console before setting this loose as a cron job/scheduled task. You don't want to be blocked because you kept sending invalid requests.
