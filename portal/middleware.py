# fBSD-Community-Portal
# Copyright (c) 2011 Nolan Lum <nol888@gmail.com>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE AUTHOR AND CONTRIBUTORS ``AS IS'' AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
# OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
# OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.

from fBSD_Portal.portal.models import CommPortalPrivMsg
from django.contrib import messages
from django.db.models import Count

class PrivMsgMiddleware(object):
    def process_view(self, request, view_func, view_args, view_kwargs):
        if not request.user.is_authenticated():
            return None

        mymsg = CommPortalPrivMsg.objects.filter(user_to=request.user)
        n_notif = mymsg.filter(notified=False).aggregate(count=Count('notified'))
        new = mymsg.filter(read=False).aggregate(count=Count('read'))

        if n_notif['count']:
            messages.warning(request, "You have %s new private message%s!" % (new['count'], '' if new['count'] == 1 else 's'))
            
            mymsg.filter(notified=False).update(notified=True)
        
        request.new_msgs = new['count']
    