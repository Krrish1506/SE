/* ============================================================
   Stark Avenue — Product Data Catalog (Dynamic)
   ============================================================ */

let PRODUCTS = [];

// Fetch products from backend securely
async function fetchProducts() {
    try {
        const response = await fetch('http://localhost:8000/products');
        if (!response.ok) throw new Error('Failed to fetch from backend');
        PRODUCTS = await response.json();
        console.log("Products loaded from backend API:", PRODUCTS);
    } catch (err) {
        console.error('Error fetching products, verify backend is running:', err);
    }
}

// Utility: find product by ID
function getProductById(id) {
    return PRODUCTS.find(p => p.id === parseInt(id)) || null;
}

// Utility: get image URL (returns as-is since URLs already include parameters)
function productImg(url, w = 800, q = 80) {
    if (!url) return '';
    if (url.includes('images.unsplash.com')) return url;
    return `${url}?w=${w}&q=${q}&fit=crop`;
}

