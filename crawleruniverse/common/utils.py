def get_ip_address(request):
    http_x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR: ", "")
    # logger.error(f'HTTP_X_FORWARDED_FOR: {http_x_forwarded_for}')
    ip = http_x_forwarded_for
    if not ip:
        ip = request.META.get('REMOTE_ADDR', "")
    remote_addr = request.META.get('REMOTE_ADDR', "")
    # logger.error(f'REMOTE_ADDR: {remote_addr}')
    client_ip = ip.split(",")[-1].strip() if ip else ""
    return http_x_forwarded_for, remote_addr, client_ip
