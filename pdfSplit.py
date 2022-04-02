from pdf2image import convert_from_path


images = convert_from_path('architecture_design_checklist.pdf', fmt="png")

for i, image in enumerate(images):
    fname = "image" + str(i) + ".png"
    print(type(image))
    image.save(fname)
