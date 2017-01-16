f = open("helloworld.html", "w")

message = """<html><head></head>
<body><p>"""+"helloworld hellowlrd"+"""<br>
come on<br><br><br>oh</p>
"""

message += """
     <fieldset>
                <legend>What is Your Favorite Pet?</legend>
                        <input type="radio" name="animal" value="Cat" />Cats<br />
                        <input type="radio" name="animal" value="Dog" />Dogs<br />
                        <input type="radio" name="animal" value="Bird" />Birds<br />
                        <input type="submit" value="Submit now" />
        </fieldset>
        <fieldset>
                <legend>What is Your Favorite Pet?</legend>
                        <input type="radio" name="animal" value="Cat" />Cats<br />
                        <input type="radio" name="animal" value="Dog" />Dogs<br />
                        <input type="radio" name="animal" value="Bird" />Birds<br />
                        <input type="submit" value="Submit now" />
        </fieldset>
</body></html>"""

f.write("""<?xml version="1.0" encoding="UTF-8"?>""")
f.write("\n")
f.write("""<QuestionForm xmlns="http://mechanicalturk.amazonaws.com/AWSMechanicalTurkDataSchemas/2005-10-01/QuestionForm.xsd">""")
f.write("\n")
f.write("""<![CDATA[""")
message = """ <h1 align="center">Rate the relevance of sentence to the comment</h1>
      <h2>Instructions</h2>"""
f.write(message)
f.write(""" ]]></FormattedContent>""")
f.close()