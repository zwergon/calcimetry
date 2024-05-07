import numpy as np
import tqdm


from calcimetry.calcimetry_api import CalcimetryAPI
from calcimetry.mongo_api import MongoAPI
from calcimetry.measurement import Measurement
from calcimetry.carrot_img import CarrotImage
from calcimetry.thumbnail import Thumbnail

COLLECTION = "datasets"


def insert_thumbnails(
    calci_api,
    img: CarrotImage,
    measure: Measurement,
    version: str,
    dim=48,
    n_images=4,
    above=True,
):
    half_dim = dim // 2
    px = img.p_x(measure.cote)

    if above:
        top_line = img.k_up
        bottom_line = img.k_arrow
    else:
        top_line = img.k_arrow
        bottom_line = img.k_down

    n_inserted = 0
    try:
        remaining_h = max(0.5 * (bottom_line.p_y(px) - top_line.p_y(px) - dim), 0)
        for _ in range(n_images):
            x_offset = np.random.uniform(low=-dim // 2, high=0)
            y_offset = np.random.uniform(low=0, high=2 * remaining_h)

            cx = px + x_offset + half_dim
            cy = top_line.p_y(px) + y_offset + half_dim

            jpg = img.vignette(dim=dim, center=(cx, cy))
            for angle in [0, 90, 180, 270]:
                jpg_rot = jpg.rotate(angle)
                thumbnail = Thumbnail(
                    version, jpg_rot, bbox=(cx, cy, dim), measurement=measure
                )

                calci_api.db[COLLECTION].insert_one(thumbnail.to_dict())
                n_inserted += 1
    except Exception as er:
        print(
            f"unable to extract thumbnail {img.image_id} at {measure.measure_id}->skip"
        )

    return n_inserted


def update_dataset(version):
    with CalcimetryAPI() as calci_api:
        measurements = calci_api.get_all_measurements()

        n_samples = 0

        for m in tqdm.tqdm(measurements):
            if int(m.quality) < 9 or float(m.val_1m) >= 85:
                continue

            IMG_ID = m.image_id

            img = calci_api.read_image(IMG_ID)
            try:
                img = img.to_resolution(0.035)

                n_samples += insert_thumbnails(calci_api, img, m, version, above=True)
                n_samples += insert_thumbnails(calci_api, img, m, version, above=False)
            except Exception as er:
                print(f"error with image {IMG_ID} : {str(er)}")


if __name__ == "__main__":
    version = "1.2"
    update_dataset(version)
