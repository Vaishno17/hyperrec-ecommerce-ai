import streamlit as st

def product_card(product):
    """
    Displays a product card with image, name, category, price,
    and discount badge (if discount > 0).
    
    Parameters:
    - product: dict with keys 'name', 'category', 'price', 'discount' (optional), 'image_url' (optional)
    """
    discount = product.get('discount', 0)
    is_discounted = discount > 0
    price = product.get('price', 0.0)
    price_after_discount = price * (1 - discount / 100) if is_discounted else price

    card_style = """
        <style>
            .product-card {
                border-radius: 12px;
                box-shadow: 0 4px 10px rgb(0 0 0 / 0.1);
                padding: 1rem;
                transition: transform 0.2s ease-in-out;
                background-color: #ffffff;
                margin-bottom: 1rem;
                display: flex;
                flex-direction: column;
                height: 100%;
                position: relative;
            }
            .product-card:hover {
                transform: translateY(-5px);
                box-shadow: 0 10px 25px rgb(0 0 0 / 0.15);
            }
            .product-image {
                width: 100%;
                max-height: 180px;
                object-fit: contain;
                margin-bottom: 0.5rem;
                background-color: #f9f9f9;
                border-radius: 8px;
            }
            .product-name {
                font-weight: 600;
                font-size: 1.1rem;
                margin-bottom: 0.25rem;
                flex-grow: 1;
            }
            .product-price {
                font-weight: 700;
                font-size: 1.1rem;
                color: #fc6767;
                margin-bottom: 0.25rem;
            }
            .product-category {
                font-size: 0.9rem;
                color: #666666;
                margin-bottom: 0.5rem;
            }
            .discount-badge {
                background-color: #ec008c;
                color: white;
                font-weight: 700;
                border-radius: 8px;
                padding: 0.2rem 0.6rem;
                font-size: 0.85rem;
                position: absolute;
                top: 10px;
                right: 10px;
                user-select: none;
            }
        </style>
    """

    st.markdown(card_style, unsafe_allow_html=True)

    st.markdown('<div class="product-card">', unsafe_allow_html=True)
    if is_discounted:
        st.markdown(f'<div class="discount-badge">-{discount}% OFF</div>', unsafe_allow_html=True)

    image_url = product.get('image_url', None)
    if image_url and isinstance(image_url, str) and image_url.strip() != '':
        st.image(image_url, use_column_width=True, clamp=True)

    st.markdown(f'<div class="product-name">{product.get("name", "Unnamed Product")}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="product-category">{product.get("category", "")}</div>', unsafe_allow_html=True)

    if is_discounted:
        st.markdown(
            f'<div class="product-price"><del>${price:.2f}</del> <span style="color:#ec008c; font-weight:700;">${price_after_discount:.2f}</span></div>',
            unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="product-price">${price:.2f}</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
