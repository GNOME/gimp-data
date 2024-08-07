import pathlib
import os
import sys

def export_scaled_img(img_width, img_height, scale):
  procedure   = Gimp.get_pdb().lookup_procedure("file-svg-load")
  config      = procedure.create_config()
  config.set_property("file", Gio.file_new_for_path('../gimp-data/images/logo/gimp-logo.svg'))
  logo_dim    = img_height * 0.75
  config.set_property("width",  logo_dim)
  config.set_property("height", logo_dim)
  Gimp.Procedure.run(procedure, config)
  v = Gimp.Procedure.run(procedure, config)

  if v.index(0) != Gimp.PDBStatusType.SUCCESS:
    sys.exit(os.EX_SOFTWARE)

  image = v.index(1)
  image.resize(img_width, img_height, (img_width-logo_dim)/2, (img_height-logo_dim)/2)
  white = Gegl.Color.new("white")
  Gimp.context_set_background(white)
  image.flatten()

  procedure = Gimp.get_pdb().lookup_procedure("file-bmp-export")
  config    = procedure.create_config()
  drawables = image.get_selected_drawables()
  # Needed otherwise it doesn't save the proper size because of bug #8855.
  drawables[0].resize_to_image_size()
  config.set_property("image", image)
  config.set_property("file", Gio.file_new_for_path('build/windows/installer/gimp.scale-' + scale + '.bmp'))
  Gimp.Procedure.run(procedure, config)

# https://jrsoftware.org/ishelp/index.php?topic=setup_wizardsmallimagefile
export_scaled_img(55, 55, '100')
export_scaled_img(64, 68, '125')
export_scaled_img(83, 80, '150')
export_scaled_img(92, 97, '175')
export_scaled_img(110, 106, '200')
export_scaled_img(119, 123, '225')
export_scaled_img(138, 140, '250')

# Avoid the images being re-generated at each build.
pathlib.Path('gimp-data/images/logo/stamp-installicon.bmp').touch()
