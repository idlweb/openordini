from django import forms
from django.conf import settings
from django.utils.safestring import mark_safe

class ColorPickerWidget(forms.TextInput):
    class Media:
        css = {
            'all': (
                settings.STATIC_URL + 'colorpicker/css/colorpicker.css',
            )
        }
        js = (
            settings.STATIC_URL + 'js/jquery-1.8.3.min.js',
            settings.STATIC_URL + 'colorpicker/js/colorpicker.js',
        )

    def __init__(self, language=None, attrs=None):
        self.language = language or settings.LANGUAGE_CODE[:2]
        super(ColorPickerWidget, self).__init__(attrs=attrs)

    def render(self, name, value, attrs=None):
        rendered = super(ColorPickerWidget, self).render(name, value, attrs)
        return rendered + mark_safe(u'''
            <script type="text/javascript">
                jQuery('#id_%s').css("background-color", "#"+jQuery('#id_%s').val());
                jQuery('#id_%s').ColorPicker({
                    onSubmit: function(hsb, hex, rgb, el) {
                        jQuery(el).val(hex);
                        jQuery(el).css("background-color", "#"+hex);
                        jQuery(el).ColorPickerHide();
                    },
                    onBeforeShow: function () {
                        code = this.value
                        if (code.length==3) code = code.charAt(0)+code.charAt(0)+code.charAt(1)+code.charAt(1)+code.charAt(2)+code.charAt(2);
                        jQuery(this).ColorPickerSetColor(code);
                    }
                }).bind('keyup', function(){
                    el = jQuery(this);
                    code = el.val();
                    hex = '#'+code;
                    var isOk  = /(^#[0-9A-F]{6}$)|(^#[0-9A-F]{3}$)/i.test(hex);
                    if (isOk) {
                        el.css("background-color", hex);
                        if (code.length==3) code = code.charAt(0)+code.charAt(0)+code.charAt(1)+code.charAt(1)+code.charAt(2)+code.charAt(2);
                        el.ColorPickerSetColor(code);
                    }
                    else if (code=="") el.css("background-color", "");
                });
            </script>
            ''' % (name, name, name))