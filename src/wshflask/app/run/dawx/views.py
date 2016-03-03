from datetime import datetime
from flask import render_template,session,redirect,url_for,flash
from flask.ext.login import login_required

from . import dawx
from ..libbase.dawxform import KaiquForm,HequForm,ChangeZoneTimeForm,MvZoneForm,DnsBindForm
from ...webclient import runcmd
from ..decorators import admin_required
from datetime import date
from ..libbase.dnsbindbase import rundns

@dawx.route('/',methods=['GET','POST'])
@dawx.route('/index.html',methods=['GET','POST'])
@login_required
@admin_required
def index():
    print 123
    return render_template('dawx/index.html')


@dawx.route('/kaiqu.html',methods=['GET','POST'])
@login_required
@admin_required
def kaiqu():
    kaiquform = KaiquForm()

    exestr = ''
    dst = ''

    if kaiquform.validate_on_submit():
        opendbnum = kaiquform.opendbnum.data
        opentime = kaiquform.opentime.data
        dst = opendbnum
        exestr='kaixinqu ' + str(opendbnum) + " " + str(opentime)

        if exestr and dst:
            res = runcmd(dst,exestr)
            flash(res)

    return render_template('dawx/kaiqu.html', kaiquform = kaiquform)

@dawx.route('/hequ.html',methods=['GET','POST'])
@login_required
@admin_required
def hequ():
    hequform = HequForm()

    exestr = ''
    dst = ''
    if hequform.validate_on_submit():
        hequip = hequform.hequip.data
        hequzone =hequform.hequzone.data

        dst = hequip
        if hequip:
            exestr='hequ ip=' + str(hequip) + " " + str(hequzone)
            print exestr
            res = runcmd(hequip, exestr)
        else:
            firstnum = str(hequzone).split()[0]
            exestr='hequ  ' + str(hequzone)
            print exestr
            res = runcmd(firstnum,exestr)

        flash(res)


    return render_template('dawx/hequ.html', hequform = hequform)



@dawx.route('/changezonetime.html',methods=['GET','POST'])
@login_required
def changezonetime():
    changezonetimeform  = ChangeZoneTimeForm()

    exestr = ''
    dst = ''

    if changezonetimeform.validate_on_submit():
        zonenum = changezonetimeform.zonenum.data
        opentime = changezonetimeform.opentime.data
        dst = zonenum
        exestr='changezonetime ' + str(zonenum) + " " + str(opentime)

        if exestr and dst:
            print exestr
            print dst
            res = runcmd(dst,exestr)
            flash(res)

    return render_template('dawx/changezonetime.html', changezonetimeform = changezonetimeform)

@dawx.route('/mvzone.html',methods=['GET','POST'])
@login_required
def mvzone():
    mvzoneform = MvZoneForm()

    exestr = ''
    dst = ''
    if mvzoneform.validate_on_submit():
        mvip = mvzoneform.mvip.data
        mvzone = mvzoneform.mvzone.data

        dst = mvip 
        exestr='mvzone ip=' + str(mvip) + " " + str(mvzone)

        if exestr and dst:
            print exestr
            print dst
            res = runcmd(dst,exestr)
            flash(res)


    return render_template('dawx/mvzone.html', mvzoneform = mvzoneform)

@dawx.route('/manage_gamezone.html',methods=['GET','POST'])
@login_required
@admin_required
def manage():
    return render_template('dawx/manage_gamezone.html')




@dawx.route('/dnsbind.html',methods=['GET','POST'])
@login_required
@admin_required
def dnsbind():
    dnsbindform = DnsBindForm()

    exestr = ''
    dst = ''

    if dnsbindform.validate_on_submit():
        unbindip = dnsbindform.unbindip.data
        bindip = dnsbindform.bindip.data
        namestart = dnsbindform.namestart.data
        nameend = dnsbindform.nameend.data
        numeval = dnsbindform.numeval.data

        if not unbindip and  not bindip:
            flash("bindip or unbindip is required")
            return  render_template('dawx/dnsbind.html',dnsbindform=dnsbindform)

        if not namestart and not nameend:
            flash("namestart or nameend is required")
            return render_template('dawx/dnsbind.html',dnsbindform=dnsbindform)
        elif not namestart:
            namestart = nameend
        elif not nameend:
            nameend = namestart

        res = rundns(unbindip,bindip,namestart,nameend,numeval)[1]
        flash(res)

    return render_template('dawx/dnsbind.html',dnsbindform=dnsbindform)

