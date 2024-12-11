from spire.presentation.common import *
from spire.presentation import *

# Create a Presentation object

presentation = Presentation()



# Load a PowerPoint presentation

presentation.LoadFromFile("Presentation/Machine Learning.pptx")

# Loop through the slides in the presentation
l = []
for i, slide in enumerate(presentation.Slides):
    # Specify the output file name

    fileName = str(i)+'.png'
    l.append(fileName)
    # Save each slide as a PNG image

    image = slide.SaveAsImage()

    image.Save(fileName)

    image.Dispose()

print(l)
