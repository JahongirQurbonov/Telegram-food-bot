// Telegram WebApp initialization
const tg = window.Telegram.WebApp
tg.expand()

// Set theme colors
document.documentElement.style.setProperty("--tg-theme-bg-color", tg.themeParams.bg_color || "#2c3e50")
document.documentElement.style.setProperty("--tg-theme-text-color", tg.themeParams.text_color || "#ffffff")

// Menu data
const menuItems = [
  { id: 1, name: "Cake", emoji: "🍰", price: 4.99, badge: "NEW", special: "star" },
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

// DOM elements
const menuGrid = document.getElementById("menuGrid")
const cartItems = document.getElementById("cartItems")
const cartCount = document.getElementById("cartCount")
const payBtn = document.getElementById("payBtn")
const orderComment = document.getElementById("orderComment")
const menuPage = document.getElementById("menuPage")
const cartPage = document.getElementById("cartPage")

// Initialize app
document.addEventListener("DOMContentLoaded", () => {
  renderMenu()
  updateCartDisplay()

  // Set up Telegram WebApp
  tg.ready()

  // Enable closing confirmation
  tg.enableClosingConfirmation()
})

// Render menu items
function renderMenu() {
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
      <div class="item-name">
        ${item.name}
        ${badgeHtml}
        ${starHtml}
      </div>
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

  // Haptic feedback
  if (tg.HapticFeedback) {
    tg.HapticFeedback.impactOccurred("light")
  }

  // Show notification
  tg.showAlert(`${item.name} added to cart!`)
}

// Remove item from cart
function removeFromCart(itemId) {
  const itemIndex = cart.findIndex((item) => item.id === itemId)
  if (itemIndex === -1) return

  if (cart[itemIndex].quantity > 1) {
    cart[itemIndex].quantity -= 1
  } else {
    cart.splice(itemIndex, 1)
  }

  updateCartDisplay()
  renderCart()

  // Haptic feedback
  if (tg.HapticFeedback) {
    tg.HapticFeedback.impactOccurred("light")
  }
}

// Update cart display
function updateCartDisplay() {
  const totalItems = cart.reduce((sum, item) => sum + item.quantity, 0)
  const total = cart.reduce((sum, item) => sum + item.price * item.quantity, 0)

  cartCount.textContent = totalItems
  cartCount.style.display = totalItems > 0 ? "flex" : "none"

  payBtn.textContent = `PAY $${total.toFixed(2)}`
  payBtn.disabled = totalItems === 0
}

// Show cart page
function showCart() {
  menuPage.style.display = "none"
  cartPage.style.display = "block"
  renderCart()

  // Update main button
  tg.MainButton.setText("Back to Menu")
  tg.MainButton.show()
  tg.MainButton.onClick(showMenu)
}

// Show menu page
function showMenu() {
  menuPage.style.display = "block"
  cartPage.style.display = "none"

  // Hide main button
  tg.MainButton.hide()
}

// Render cart items
function renderCart() {
  if (cart.length === 0) {
    cartItems.innerHTML = `
      <div class="empty-cart">
        <div class="empty-cart-emoji">🛒</div>
        <h3>Your cart is empty</h3>
        <p>Add some delicious items from our menu!</p>
      </div>
    `
    return
  }

  cartItems.innerHTML = ""

  cart.forEach((item) => {
    const cartItemDiv = document.createElement("div")
    cartItemDiv.className = "cart-item"

    cartItemDiv.innerHTML = `
      <div class="cart-item-info">
        <span class="cart-item-emoji">${item.emoji}</span>
        <div class="cart-item-details">
          <h3>${item.name} ${item.quantity > 1 ? `${item.quantity}x` : ""}</h3>
          <p>Meat™</p>
          <div class="quantity-controls">
            <button class="quantity-btn" onclick="removeFromCart(${item.id})">-</button>
            <span class="quantity-display">${item.quantity}</span>
            <button class="quantity-btn" onclick="addToCart(${item.id})">+</button>
          </div>
        </div>
      </div>
      <div class="cart-item-price">$${(item.price * item.quantity).toFixed(2)}</div>
    `

    cartItems.appendChild(cartItemDiv)
  })
}

// Process order
function processOrder() {
  console.log("🔍 processOrder() called")
  
  if (cart.length === 0) {
    console.log("❌ Cart is empty")
    tg.showAlert("Your cart is empty!")
    return
  }

  const comment = orderComment.value.trim()
  const total = cart.reduce((sum, item) => sum + item.price * item.quantity, 0)

  const orderData = {
    cart: cart,
    total: total,
    comment: comment,
    timestamp: new Date().toISOString(),
    user: tg.initDataUnsafe.user || {},
  }

  console.log("📤 Sending order data:", orderData)
  console.log("📤 JSON string:", JSON.stringify(orderData))
  
  // Telegram WebApp mavjudligini tekshirish
  if (!window.Telegram || !window.Telegram.WebApp) {
    console.error("❌ Telegram WebApp not available")
    alert("Telegram WebApp not available!")
    return
  }
  
  console.log("✅ Telegram WebApp available")
  console.log("🔍 tg object:", tg)
  
  try {
    // Send data to Telegram bot
    tg.sendData(JSON.stringify(orderData))
    console.log("✅ Data sent successfully")
    
    // Show success message
    tg.showAlert("Order sent successfully!")
    
  } catch (error) {
    console.error("❌ Error sending data:", error)
    alert("Error sending order: " + error.message)
  }

  // Haptic feedback
  if (tg.HapticFeedback) {
    tg.HapticFeedback.notificationOccurred("success")
  }
}

// Close app
function closeApp() {
  tg.close()
}

// Handle back button
tg.onEvent("backButtonClicked", () => {
  if (cartPage.style.display !== "none") {
    showMenu()
  } else {
    tg.close()
  }
})

// Show back button when in cart
function updateBackButton() {
  if (cartPage.style.display !== "none") {
    tg.BackButton.show()
  } else {
    tg.BackButton.hide()
  }
}

// Update back button visibility
const observer = new MutationObserver(() => {
  updateBackButton()
})

observer.observe(cartPage, { attributes: true, attributeFilter: ["style"] })
