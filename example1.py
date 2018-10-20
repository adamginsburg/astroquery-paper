# Create a finder chart and overlay two catalogs using the Vizier and SkyView
# tools
from astropy import units as u
from astropy.coordinates import SkyCoord
from astropy.wcs import WCS
from astroquery.skyview import SkyView
from astroquery.vizier import Vizier
import matplotlib.pyplot as plt

center = SkyCoord.from_name("Orion KL")

# Grab an image from SkyView of the Orion KL nebula region
imglist = SkyView.get_images(position=center, survey="2MASS-J")

# The returned value is a list of images, but there is only one
img = imglist[0]

# "img" is now a fits.HDUList object; the 0th entry is the image
mywcs = WCS(img[0].header)

fig = plt.figure(1)
fig.clf()  # Just in case one was open before
# Use astropy's wcsaxes tool to create an RA/Dec image
ax = fig.add_axes([0.15, 0.1, 0.8, 0.8], projection=mywcs)
ax.set_xlabel("RA")
ax.set_ylabel("Dec")

ax.imshow(img[0].data, cmap="gray_r", interpolation="none", origin="lower",
          norm=plt.matplotlib.colors.LogNorm())

# Retrieve a specific table from Vizier to overplot
tablelist = Vizier.query_region(
    center, radius=5*u.arcmin, catalog="J/ApJ/826/16/table1")
# Again, the result is a list of tables, so we"ll get the first one
result = tablelist[0]

# Convert the ra/dec entries in the table to astropy coordinates
tbl_crds = SkyCoord(result["RAJ2000"], result["DEJ2000"],
                    unit=(u.hour, u.deg), frame="fk5")

# We want this table too:
tablelist2 = Vizier(row_limit=10000).query_region(
    center, radius=5*u.arcmin, catalog="J/ApJ/540/236")
result2 = tablelist2[0]
tbl_crds2 = SkyCoord(result2["RAJ2000"], result2["DEJ2000"],
                     unit=(u.hour, u.deg), frame="fk5")

# Overplot the data in the image
ax.plot(tbl_crds.ra, tbl_crds.dec, "*", transform=ax.get_transform("fk5"),
        mec="b", mfc="none")
ax.plot(tbl_crds2.ra, tbl_crds2.dec, "o", transform=ax.get_transform("fk5"),
        mec="r", mfc="none")
# Zoom in on the relevant region
ax.axis([100,200,100,200])

plt.show()
