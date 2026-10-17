document.addEventListener("DOMContentLoaded", () => {
    const navigation = document.querySelector(".navbar nav");
    const navToggle = document.querySelector(".nav-toggle");
    const searchToggle = document.querySelector(".search-toggle");
    const searchForm = document.querySelector("#site-search");
    const searchInput = document.querySelector("#menu-search");
    const cartPanel = document.querySelector("#cart-panel");
    const cartToggle = document.querySelector(".cart-toggle");
    const cartClose = document.querySelector(".cart-close");
    const cartList = document.querySelector(".cart-items");
    const cartEmpty = document.querySelector(".cart-empty");
    const cartCount = document.querySelector(".cart-count");
    const cartTotal = document.querySelector(".cart-total strong");
    const cartDataInput = document.querySelector("#cart-data");
    const checkoutSummary = document.querySelector("#checkout-summary");
    const money = new Intl.NumberFormat("en-KE", { maximumFractionDigits: 2 });

    const readCart = () => {
        try {
            const savedCart = JSON.parse(localStorage.getItem("festoveCart") || "[]");
            return Array.isArray(savedCart) ? savedCart : [];
        } catch {
            return [];
        }
    };
    let cart = readCart();
    const saveCart = () => {
        try {
            localStorage.setItem("festoveCart", JSON.stringify(cart));
        } catch {
            // The current page cart still works if browser storage is unavailable.
        }
    };

    if (document.querySelector("[data-order-success]")) {
        cart = [];
        try { localStorage.removeItem("festoveCart"); } catch { /* Storage may be unavailable. */ }
    }

    if (navigation && navToggle) {
        const navIcon = navToggle.querySelector("i");
        const setMenuOpen = (isOpen) => {
            navigation.classList.toggle("is-open", isOpen);
            navToggle.setAttribute("aria-expanded", String(isOpen));
            navToggle.setAttribute("aria-label", isOpen ? "Close navigation menu" : "Open navigation menu");
            navIcon?.classList.toggle("fa-bars", !isOpen);
            navIcon?.classList.toggle("fa-xmark", isOpen);
        };
        navToggle.addEventListener("click", () => {
            setMenuOpen(navToggle.getAttribute("aria-expanded") !== "true");
        });
        navigation.querySelectorAll(".nav-links a, .nav-actions a").forEach((link) => {
            link.addEventListener("click", () => setMenuOpen(false));
        });
    }

    if (searchToggle && searchForm) {
        const setSearchOpen = (isOpen) => {
            searchForm.hidden = !isOpen;
            searchToggle.setAttribute("aria-expanded", String(isOpen));
            searchToggle.setAttribute("aria-label", isOpen ? "Close search" : "Open search");
            if (isOpen) searchInput?.focus();
        };
        searchToggle.addEventListener("click", () => setSearchOpen(searchForm.hidden));
        document.addEventListener("keydown", (event) => {
            if (event.key === "Escape") setSearchOpen(false);
        });
    }

    const renderCart = () => {
        const itemCount = cart.reduce((sum, item) => sum + item.quantity, 0);
        const total = cart.reduce((sum, item) => sum + item.price * item.quantity, 0);

        if (cartCount) cartCount.textContent = itemCount;
        if (cartTotal) cartTotal.textContent = `Ksh ${money.format(total)}`;
        if (!cartList) return;

        cartList.replaceChildren();
        cart.forEach((item) => {
            const row = document.createElement("li");
            row.className = "cart-item";
            const details = document.createElement("span");
            details.textContent = `${item.name} × ${item.quantity} — Ksh ${money.format(item.price * item.quantity)}`;
            const remove = document.createElement("button");
            remove.type = "button";
            remove.className = "cart-remove";
            remove.dataset.remove = item.id;
            remove.setAttribute("aria-label", `Remove ${item.name} from cart`);
            remove.textContent = "Remove";
            row.append(details, remove);
            cartList.append(row);
        });
        if (cartEmpty) cartEmpty.hidden = cart.length > 0;
        cartList.hidden = cart.length === 0;
        saveCart();
    };

    if (cartPanel && cartToggle) {
        const setCartOpen = (isOpen) => {
            cartPanel.hidden = !isOpen;
            cartToggle.setAttribute("aria-expanded", String(isOpen));
            cartToggle.setAttribute("aria-label", isOpen ? "Close cart" : "Open cart");
        };
        cartToggle.addEventListener("click", () => setCartOpen(cartPanel.hidden));
        cartClose?.addEventListener("click", () => setCartOpen(false));
        cartPanel.addEventListener("click", (event) => {
            const removeButton = event.target.closest("[data-remove]");
            if (!removeButton) return;
            cart = cart.filter((item) => item.id !== removeButton.dataset.remove);
            renderCart();
        });

        document.querySelectorAll(".cart-link").forEach((button) => {
            button.addEventListener("click", () => {
                const card = button.closest(".menu-item-card");
                if (!card) return;
                const item = {
                    id: button.dataset.productId,
                    name: card.querySelector("h3")?.textContent.trim() || "Menu item",
                    price: Number(button.dataset.productPrice),
                };
                if (!item.id || !Number.isFinite(item.price)) return;
                const existingItem = cart.find((cartItem) => cartItem.id === item.id);
                if (existingItem) existingItem.quantity += 1;
                else cart.push({ ...item, quantity: 1 });
                renderCart();
                setCartOpen(true);
            });
        });
        renderCart();
    }

    if (cartDataInput) cartDataInput.value = JSON.stringify(cart);
    if (checkoutSummary) {
        checkoutSummary.replaceChildren();
        if (cart.length === 0) {
            checkoutSummary.textContent = "Your cart is empty. Add items from the menu before checkout.";
        } else {
            cart.forEach((item) => {
                const line = document.createElement("p");
                line.textContent = `${item.name} × ${item.quantity} — Ksh ${money.format(item.price * item.quantity)}`;
                checkoutSummary.append(line);
            });
            const total = cart.reduce((sum, item) => sum + item.price * item.quantity, 0);
            const totalLine = document.createElement("strong");
            totalLine.textContent = `Total: Ksh ${money.format(total)}`;
            checkoutSummary.append(totalLine);
        }
    }

    const filterLinks = document.querySelectorAll(".food-lists a[data-filter]");
    const menuCards = document.querySelectorAll(".menu-item-card[data-category]");
    filterLinks.forEach((link) => {
        link.addEventListener("click", (event) => {
            event.preventDefault();
            const filter = link.dataset.filter;
            filterLinks.forEach((item) => item.classList.remove("is-active"));
            link.classList.add("is-active");
            menuCards.forEach((card) => {
                card.hidden = filter !== "all" && card.dataset.category !== filter;
            });
        });
    });

    document.addEventListener("keydown", (event) => {
        if (event.key === "Escape" && navigation && navToggle) {
            navigation.classList.remove("is-open");
            navToggle.setAttribute("aria-expanded", "false");
            navToggle.setAttribute("aria-label", "Open navigation menu");
            const navIcon = navToggle.querySelector("i");
            navIcon?.classList.add("fa-bars");
            navIcon?.classList.remove("fa-xmark");
        }
    });
});
