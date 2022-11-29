certbot certonly --dns-cloudflare --dns-cloudflare-credentials /root/.secrets/cloudflare.ini -d crowflock.com,*.crowflock.com --preferred-challenges dns-01 --force-renewal
alias cp=cp
#[root@vortex crowflock.com]# ls
#cert.pem  chain.pem  fullchain.pem  privkey.pem  README
#[root@vortex crowflock.com]# pwd
cp -f /etc/letsencrypt/live/crowflock.com/fullchain.pem /etc/traefik/certs/selfsigned.crt
cp -f /etc/letsencrypt/live/crowflock.com/privkey.pem /etc/traefik/certs/selfsigned.key
cp -f /etc/letsencrypt/live/crowflock.com/fullchain.pem /root/traefik/certs/selfsigned.crt
cp -f /etc/letsencrypt/live/crowflock.com/privkey.pem /root/traefik/certs/selfsigned.key
docker restart traefik-traefik-1
docker restart passbolt-passbolt-1
