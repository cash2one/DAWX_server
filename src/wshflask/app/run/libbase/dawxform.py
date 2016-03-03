#coding=utf-8
from flask.ext.wtf import Form
from wtforms import StringField,SubmitField,IntegerField,TextField
from wtforms.validators import Required
from  datetime import date




class BaseForm(Form):
    LANGUAGES=['zh']

class NameForm(Form):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')

class KaiquForm(BaseForm):
    opendbnum = IntegerField(u'游戏区号',default=123,validators=[Required()])
    opentime  = IntegerField(u'开区时间',default=int(date.today().__format__("%Y%m%d")),validators=[Required()])
    submit = SubmitField('Submit')


class HequForm(BaseForm):
    hequip = StringField(u'合区目的ip', validators = [])
    hequzone = StringField(u'游戏区号列表', validators = [Required()])
    submit = SubmitField('Submit')

class ChangeZoneTimeForm(BaseForm):
     zonenum = IntegerField(u'游戏区号',default=123,validators=[Required()])
     opentime  = IntegerField(u'需要重新设置的时间',default=int(date.today().__format__("%Y%m%d")),validators=[Required()])
     submit = SubmitField('Submit')


class MvZoneForm(BaseForm):
    mvip = StringField(u'要迁移到的ip', validators = [Required()])
    mvzone = StringField(u'游戏区号列表', validators = [Required()])
    submit = SubmitField('Submit')

class addgamezone(BaseForm):
    dbnum = StringField("dbnum", validators = [Required()])
    dbvalue = StringField('dbvalue', validators = [Required()])
    webip = StringField('webip', validators = [Required()])
    submit = SubmitField('Submit')


class DnsBindForm(BaseForm):
    unbindip = StringField(u'解绑的服务器ip',validators = [])
    bindip = StringField(u'绑定的服务器ip',validators = [])
    namestart = StringField(u'起始域名(后缀app1101376335.qqopenapp.com不需要写)',validators=[])
    nameend = StringField(u'结束域名(后缀app1101376335.qqopenapp.com不需要写)',validators=[])
    numeval = IntegerField(u'间隔',default=1,validators=[Required()])
    submit = SubmitField('Submit')

