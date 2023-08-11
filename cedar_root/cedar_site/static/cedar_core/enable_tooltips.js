

/* Enable Tooltips */

// Enable tooltips for all fields where attribute data-bs-toggle="tooltip".
// Use in conjunction with 

$(document).ready(function () {
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    })

});





/* 

    ENABLE TOOLTIPS FOR ALL FORM FIELDS

    Add this code to a form object to enable tooltips for all form fields.

    def __init__(self, *args, **kwargs):
    super(FORMNAME, self).__init__(*args, **kwargs)
    for field in self.fields:
        help_text = self.fields[field].help_text
        self.fields[field].help_text = None
        if help_text != '':
            self.fields[field].widget.attrs.update({'data-bs-toggle':"tooltip", 'data-placement':'top', 'data-bs-title':help_text}) 


*/