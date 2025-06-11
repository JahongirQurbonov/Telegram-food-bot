// Telegram WebApp initialization
const tg = window.Telegram.WebApp
tg.expand()

// Menu data
const menuItems = [
  { id: 1, name: "Cake", emoji: "🍰", price: 1.0, badge: "NEW", special: "star" },
  { id: 2, name: "Burger", emoji: "🍔", price: 4.99 },
  { id: 3, name: "Fries", emoji: "🍟", price: 1.49 },
  { id: 4, name: "Hotdog", emoji: "🌭", price: 3.49 },
  { id: 5, name: "Taco", emoji: "🌮", price: 3.99 },
  { id: 6, name: "Pizza", emoji: "🍕", price: 7.99 },
  { id: 7, name: "Donut", emoji: "🍩", price: 1.49 },
  { id: 8, name: "Popcorn", emoji: "🍿", price: 1.99 },
  { id: 9, name: "Coke", emoji: "🥤", price: 1.49 },
  { id: 10, name: "Icecream", emoji: "🍦", price: 5.99 },
  { id: 11, name: "Cookie", emoji: "🍪", price: 3.99 },
  { id: 12, name: "Flan", emoji: "🍮", price: 7.99 },
]

// Cart state
const cart = []

// Initialize app
document.addEventListener("DOMContentLoaded", () => {
  renderMenu()
  updateCartDisplay()
})

// Render menu items
function renderMenu() {
  const menuGrid = document.getElementById("menuGrid")
  menuGrid.innerHTML = ""

  menuItems.forEach((item) => {
    const menuItemDiv = document.createElement("div")
    menuItemDiv.className = "menu-item"

    const badgeHtml = item.badge ? `<span class="new-badge">${item.badge}</span>` : ""
    const starHtml = item.special === "star" ? '<span class="star-badge">⭐</span>' : ""
    const buttonClass = item.badge === "NEW" ? "buy-btn" : "add-btn"
    const buttonText = item.badge === "NEW" ? "BUY" : "ADD"

    menuItemDiv.innerHTML = `
            <span class="item-emoji">${item.emoji}</span>
            <div class="item-name">${item.name}${badgeHtml}${starHtml}</div>
            <div class="item-price">$${item.price.toFixed(2)}</div>
            <button class="${buttonClass}" onclick="addToCart(${item.id})">${buttonText}</button>
        `

    menuGrid.appendChild(menuItemDiv)
  })
}

// Add item to cart
function addToCart(itemId) {
  const item = menuItems.find((i) => i.id === itemId)
  const existingItem = cart.find((i) => i.id === itemId)

  if (existingItem) {
    existingItem.quantity += 1
  } else {
    cart.push({
      id: item.id,
      name: item.name,
      emoji: item.emoji,
      price: item.price,
      quantity: 1,
    })
  }

  updateCartDisplay()
  showCart()
}

// Show cart view
function showCart() {
  document.querySelector(".main-content").style.display = "none"
  document.getElementById("cartSummary").style.display = "block"
  renderCart()
}

// Show menu view
function showMenu() {
  document.querySelector(".main-content").style.display = "block"
  document.getElementById("cartSummary").style.display = "none"
}

// Render cart items
function renderCart() {
  const cartItemsDiv = document.getElementById("cartItems")
  cartItemsDiv.innerHTML = ""

  cart.forEach((item) => {
    const cartItemDiv = document.createElement("div")
    cartItemDiv.className = "cart-item"

    cartItemDiv.innerHTML = `
            <div class="cart-item-info">
                <span class="cart-item-emoji">${item.emoji}</span>
                <div class="cart-item-details">
                    <h3>${item.name} ${item.quantity}x</h3>
                    <p>Meat™</p>
                </div>
            </div>
            <div class="cart-item-price">$${(item.price * item.quantity).toFixed(2)}</div>
        `

    cartItemsDiv.appendChild(cartItemDiv)
  })
}

// Update cart display
function updateCartDisplay() {
  const total = cart.reduce((sum, item) => sum + item.price * item.quantity, 0)
  const payBtn = document.getElementById("payBtn")
  if (payBtn) {
    payBtn.textContent = `PAY $${total.toFixed(2)}`
  }
}

// Process order
function processOrder() {
  const comment = document.getElementById("orderComment").value
  const total = cart.reduce((sum, item) => sum + item.price * item.quantity, 0)

  const orderData = {
    cart: cart,
    total: total,
    comment: comment,
    timestamp: new Date().toISOString(),
  }

  // Send data to Telegram bot
  tg.sendData(JSON.stringify(orderData))
}

// Close app
function closeApp() {
  tg.close()
}

// Set main button
if (cart.length > 0) {
  tg.MainButton.setText("VIEW CART")
  tg.MainButton.show()
  tg.MainButton.onClick(showCart)
}
