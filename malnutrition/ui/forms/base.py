# for the user interface in this site
# we are using blueprint css and that
# expects forms to be presented in a certain way
# this code sets the HTML in that manner
# 
# its useful to have a base class for all forms anyway
# so this isn't too bad
from django import forms

def as_blue_print(self):
    return self._html_output(u"""
    <div>
        
        <div>%(label)s %(errors)s</div>
        <div>%(field)s</div>
        <div class="help">%(help_text)s</div>
    </div>
    """, u'%s', '', u'%s', False)

class BaseForm(forms.Form):
    def as_custom(self):
        return as_blue_print(self)

class BaseModelForm(forms.ModelForm):
    def as_custom(self):
        return as_blue_print(self)

# this is a little worse, but it pushes an as_div into the form
# which is then set as the default so the errors come out nicely
from django.utils.html import conditional_escape
from django.utils.encoding import smart_unicode, StrAndUnicode, force_unicode
from django.utils.safestring import mark_safe
        
def as_div(self):
    if not self: return u''
    return mark_safe(u'<span class="field-error">%s</span>'
            % ''.join([u'%s<br />' % conditional_escape(force_unicode(e)) for e in self]))
            
forms.util.ErrorList.__unicode__ = as_div