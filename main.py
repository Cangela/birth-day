import webapp2
import birthday
import cgi

form="""
<form method="post">
    <strong>What is your birthday?</strong>
    <br>
    <br>
    <label>
        <b>Month</b>
        <input type="text" name="month" value="%(month)s">
    </label>
    <label>
        <b>Day</b>
        <input type="text" name="day" value="%(day)s">
    </label>
    <label>
        <b>Year</b>
        <input type="text" name="year" value="%(year)s">
    </label>
    <br>
    <br>
    <div style="color: red"><b>%(error)s</b></div>
    <br>
    <br>
    <input type="submit">
</form>
"""
def escape_html(s):
    return cgi.escape(s, quote=True)

class MainPage(webapp2.RequestHandler):
    def write_form(self, error="", month="", day="", year=""):
        self.response.out.write(form % {"error": error,
                                        "month": escape_html(month),
                                        "day": escape_html(day),
                                        "year": escape_html(year)})

    def get(self):
        self.write_form()

    def post(self):
        user_month = self.request.get('month')
        user_day = self.request.get('day')
        user_year = self.request.get('year')

        month = birthday.valid_month(user_month)
        day = birthday.valid_day(user_day)
        year = birthday.valid_year(user_year)

        if not (month and day and year):
            self.write_form("That doesn't look valid to me, friend.",
            user_month, user_day, user_year)
        else:
            self.redirect("/thanks")

class ThanksHandler(webapp2.RequestHandler):
    def get(self):
        self.response.out.write("Thanks! That's a totally valid day!")



app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/thanks', ThanksHandler)
], debug=True)
