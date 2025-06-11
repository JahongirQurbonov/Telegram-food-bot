// Telegram WebApp initialization
console.log("🚀 Script started loading...")

const tg = window.Telegram?.WebApp
console.log("🔍 Telegram object:", window.Telegram)
console.log("🔍 WebApp object:", tg)

if (tg) {
  tg.expand()
  console.log("✅ WebApp expanded")
} else {
  console.error("❌ Telegram WebApp not found!")
}

// Set theme colors
if (tg?.themeParams) {
  document.documentElement.style.setProperty("--tg-theme-bg-color", tg.themeParams.bg_color || "#2c3e50")
  document.documentElement.style.setProperty("--tg-theme-text-color", tg.themeParams.text_color || "#ffffff")
  console.log("✅ Theme colors set")
}

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
let menuGrid, cartItems, cartCount, payBtn, orderComment, menuPage, cartPage

// Initialize app
document.addEventListener("DOMContentLoaded", () => {
  console.log("📄 DOM loaded")

  // Get DOM elements
  menuGrid = document.getElementById("menuGrid")
  cartItems = document.getElementById("cartItems")
  cartCount = document.getElementById("cartCount")
  payBtn = document.getElementById("payBtn")
  orderComment = document.getElementById("orderComment")
  menuPage = document.getElementById("menuPage")
  cartPage = document.getElementById("cartPage")

  console.log("🔍 DOM elements:", {
    menuGrid: !!menuGrid,
    cartItems: !!cartItems,
    cartCount: !!cartCount,
    payBtn: !!payBtn,
    orderComment: !!orderComment,
    menuPage: !!menuPage,
    cartPage: !!cartPage,
  })

  if (!payBtn) {
    console.error("❌ PAY button not found!")
    return
  }

  // Add click event listener to PAY button
  payBtn.addEventListener("click", (event) => {
    console.log("🔥 PAY button clicked!")
    event.preventDefault()
    processOrder()
  })

  renderMenu()
  updateCartDisplay()

  // Set up Telegram WebApp
  if (tg) {
    tg.ready()
    console.log("✅ Telegram WebApp ready")

    // Enable closing confirmation
    tg.enableClosingConfirmation()
    console.log("✅ Closing confirmation enabled")
  }
})

// Render menu items
function renderMenu() {
  console.log("🍽️ Rendering menu...")

  if (!menuGrid) {
    console.error("❌ Menu grid not found!")
    return
  }

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

  console.log(`✅ Menu rendered with ${menuItems.length} items`)
}

// Add item to cart
function addToCart(itemId) {
  console.log(`🛒 Adding item ${itemId} to cart`)

  const item = menuItems.find((i) => i.id === itemId)
  if (!item) {
    console.error(`❌ Item ${itemId} not found!`)
    return
  }

  const existingItem = cart.find((i) => i.id === itemId)

  if (existingItem) {
    existingItem.quantity += 1
    console.log(`📈 Increased quantity for ${item.name}: ${existingItem.quantity}`)
  } else {
    cart.push({
      id: item.id,
      name: item.name,
      emoji: item.emoji,
      price: item.price,
      quantity: 1,
    })
    console.log(`➕ Added new item to cart: ${item.name}`)
  }

  updateCartDisplay()

  // Haptic feedback
  if (tg?.HapticFeedback) {
    tg.HapticFeedback.impactOccurred("light")
    console.log("📳 Haptic feedback triggered")
  }

  // Show notification
  if (tg?.showAlert) {
    tg.showAlert(`${item.name} added to cart!`)
    console.log(`🔔 Alert shown: ${item.name} added`)
  } else {
    alert(`${item.name} added to cart!`)
  }
}

// Remove item from cart
function removeFromCart(itemId) {
  console.log(`🗑️ Removing item ${itemId} from cart`)

  const itemIndex = cart.findIndex((item) => item.id === itemId)
  if (itemIndex === -1) {
    console.error(`❌ Item ${itemId} not found in cart!`)
    return
  }

  if (cart[itemIndex].quantity > 1) {
    cart[itemIndex].quantity -= 1
    console.log(`📉 Decreased quantity for ${cart[itemIndex].name}: ${cart[itemIndex].quantity}`)
  } else {
    const removedItem = cart.splice(itemIndex, 1)[0]
    console.log(`➖ Removed item from cart: ${removedItem.name}`)
  }

  updateCartDisplay()
  renderCart()

  // Haptic feedback
  if (tg?.HapticFeedback) {
    tg.HapticFeedback.impactOccurred("light")
  }
}

// Update cart display
function updateCartDisplay() {
  const totalItems = cart.reduce((sum, item) => sum + item.quantity, 0)
  const total = cart.reduce((sum, item) => sum + item.price * item.quantity, 0)

  console.log(`🔄 Updating cart display: ${totalItems} items, $${total.toFixed(2)}`)

  if (cartCount) {
    cartCount.textContent = totalItems
    cartCount.style.display = totalItems > 0 ? "flex" : "none"
  }

  if (payBtn) {
    payBtn.textContent = `PAY $${total.toFixed(2)}`
    payBtn.disabled = totalItems === 0
    console.log(`💰 PAY button updated: ${payBtn.textContent}, disabled: ${payBtn.disabled}`)
  }
}

// Show cart page
function showCart() {
  console.log("🛒 Showing cart page")

  if (menuPage && cartPage) {
    menuPage.style.display = "none"
    cartPage.style.display = "block"
    renderCart()
  }

  // Update main button
  if (tg?.MainButton) {
    tg.MainButton.setText("Back to Menu")
    tg.MainButton.show()
    tg.MainButton.onClick(showMenu)
  }
}

// Show menu page
function showMenu() {
  console.log("🍽️ Showing menu page")

  if (menuPage && cartPage) {
    menuPage.style.display = "block"
    cartPage.style.display = "none"
  }

  // Hide main button
  if (tg?.MainButton) {
    tg.MainButton.hide()
  }
}

// Render cart items
function renderCart() {
  console.log("🛒 Rendering cart items")

  if (!cartItems) {
    console.error("❌ Cart items container not found!")
    return
  }

  if (cart.length === 0) {
    cartItems.innerHTML = `
      <div class="empty-cart">
        <div class="empty-cart-emoji">🛒</div>
        <h3>Your cart is empty</h3>
        <p>Add some delicious items from our menu!</p>
      </div>
    `
    console.log("📭 Cart is empty")
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

  console.log(`✅ Cart rendered with ${cart.length} items`)
}

// Process order - MAIN FUNCTION
function processOrder() {
  console.log("🔥🔥🔥 processOrder() CALLED! 🔥🔥🔥")

  if (cart.length === 0) {
    console.log("❌ Cart is empty")
    if (tg?.showAlert) {
      tg.showAlert("Your cart is empty!")
    } else {
      alert("Your cart is empty!")
    }
    return
  }

  const comment = orderComment?.value?.trim() || ""
  const total = cart.reduce((sum, item) => sum + item.price * item.quantity, 0)

  const orderData = {
    cart: cart,
    total: total,
    comment: comment,
    timestamp: new Date().toISOString(),
    user: tg?.initDataUnsafe?.user || {},
  }

  console.log("📤 Order data prepared:", orderData)
  console.log("📤 JSON string:", JSON.stringify(orderData))

  // Telegram WebApp mavjudligini tekshirish
  if (!window.Telegram || !window.Telegram.WebApp) {
    console.error("❌ Telegram WebApp not available")
    alert("Telegram WebApp not available!")
    return
  }

  console.log("✅ Telegram WebApp available")
  console.log("🔍 tg object:", tg)
  console.log("🔍 tg.sendData function:", typeof tg.sendData)

  try {
    // Send data to Telegram bot
    console.log("📤 Calling tg.sendData()...")
    tg.sendData(JSON.stringify(orderData))
    console.log("✅ tg.sendData() called successfully")

    // Show success message
    if (tg.showAlert) {
      tg.showAlert("Order sent successfully!")
    } else {
      alert("Order sent successfully!")
    }
  } catch (error) {
    console.error("❌ Error sending data:", error)
    alert("Error sending order: " + error.message)
  }

  // Haptic feedback
  if (tg?.HapticFeedback) {
    tg.HapticFeedback.notificationOccurred("success")
    console.log("📳 Success haptic feedback triggered")
  }
}

// Close app
function closeApp() {
  console.log("❌ Closing app")
  if (tg?.close) {
    tg.close()
  }
}

// Handle back button
if (tg) {
  tg.onEvent("backButtonClicked", () => {
    console.log("⬅️ Back button clicked")
    if (cartPage && cartPage.style.display !== "none") {
      showMenu()
    } else {
      tg.close()
    }
  })
}

// Show back button when in cart
function updateBackButton() {
  if (cartPage && cartPage.style.display !== "none") {
    tg?.BackButton?.show()
  } else {
    tg?.BackButton?.hide()
  }
}

// Update back button visibility
if (cartPage) {
  const observer = new MutationObserver(() => {
    updateBackButton()
  })
  observer.observe(cartPage, { attributes: true, attributeFilter: ["style"] })
}

// Global error handler
window.addEventListener("error", (event) => {
  console.error("🚨 Global error:", event.error)
  console.error("🚨 Error message:", event.message)
  console.error("🚨 Error source:", event.filename, "line:", event.lineno)
})

console.log("✅ Script loaded completely")
