import io
import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.colormasks import SolidFillColorMask


def generate_qr_code_image(target_url, fill_color=(244, 63, 94), back_color=(15, 23, 42)):
    """
    Generates a high-resolution PNG QR Code image for a given URL.
    :param target_url: Absolute URL string to encode into QR code.
    :param fill_color: RGB tuple for foreground modules (default: Rose-500).
    :param back_color: RGB tuple for background (default: Slate-900).
    :return: BytesIO buffer containing PNG image data.
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=3,
    )
    qr.add_data(target_url)
    qr.make(fit=True)

    img = qr.make_image(
        image_factory=StyledPilImage,
        color_mask=SolidFillColorMask(back_color=back_color, front_color=fill_color)
    )

    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer
