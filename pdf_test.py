import pdfkit 

htmlstr = '<h2>Heading 2</h2><p>Sample paragraph.</p>'

pdfkit.from_string(htmlstr, 'sample.pdf') 
