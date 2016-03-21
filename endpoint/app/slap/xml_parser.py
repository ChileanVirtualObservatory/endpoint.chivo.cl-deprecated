from astropy.io.votable.tree import VOTableFile, Resource, Table, Field
import StringIO
# Create a new VOTable file...
votable = VOTableFile()

# ...with one resource...
resource = Resource()
votable.resources.append(resource)

# ... with one table
table = Table(votable)
resource.tables.append(table)

# Define some fields
table.fields.extend([
        Field(votable, name="filename", datatype="char", arraysize="*"),
        Field(votable, name="matrix", datatype="double", arraysize="2x2")])

# Now, use those field definitions to create the numpy record arrays, with
# the given number of rows
table.create_arrays(2)

# Now table.array can be filled with data
table.array[0] = ('test1.xml', [[1, 0], [0, 1]])
table.array[1] = ('test2.xml', [[0.5, 0.3], [0.2, 0.1]])

# Now write the whole thing to a file.
# Note, we have to use the top-level votable file object
a = StringIO.StringIO()
votable.to_xml(a)
print a.getvalue()