document.addEventListener('DOMContentLoaded', function() {
    // Navigation handling
    document.getElementById('nav-orders').addEventListener('click', showOrderForm);
    document.getElementById('nav-portfolios').addEventListener('click', showPortfolios);
    document.getElementById('back-to-portfolios').addEventListener('click', showPortfolios);
    document.getElementById('error-back').addEventListener('click', showOrderForm);
    
    // Order form submission
    document.getElementById('order-form').addEventListener('submit', handleOrderSubmission);
    
    // Initial view
    showOrderForm();
    
    // Functions
    function showOrderForm() {
        console.log("Loading order form... ");
        setActiveNavItem('nav-orders');
        hideAllSections();
        document.getElementById('order-section').style.display = 'block';
    }
    
    function showPortfolios() {
        console.log("Loading portfolios... ");
        setActiveNavItem('nav-portfolios');
        hideAllSections();
        document.getElementById('portfolios-section').style.display = 'block';
        loadPortfolios();
    }
    
    function showPortfolioDetail(userId) {
        console.log("Loading portfolio for user:", userId);
        hideAllSections();
        document.getElementById('portfolio-detail-section').style.display = 'block';
        loadPortfolioDetail(userId);
    }
    
    function showError(message) {
        hideAllSections();
        document.getElementById('error-message').textContent = message;
        document.getElementById('error-section').style.display = 'block';
    }
    
    function hideAllSections() {
        document.getElementById('order-section').style.display = 'none';
        document.getElementById('portfolios-section').style.display = 'none';
        document.getElementById('portfolio-detail-section').style.display = 'none';
        document.getElementById('error-section').style.display = 'none';
    }
    
    function setActiveNavItem(id) {
        document.querySelectorAll('nav a').forEach(a => a.classList.remove('active'));
        document.getElementById(id).classList.add('active');
    }
    
    async function handleOrderSubmission(event) {
        event.preventDefault();
        
        const form = event.target;
        const resultElement = document.getElementById('order-result');
        resultElement.innerHTML = '<p class="loading">Processing order...</p>';
        
        const formData = {
            user_id: form.user_id.value,
            symbol: form.symbol.value,
            order_type: form.order_type.value,
            quantity: parseInt(form.quantity.value),
            price: parseFloat(form.price.value)
        };
        
        try {
            const response = await fetch(`${CONFIG.orderServiceUrl}/orders`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formData)
            });
            
            const result = await response.json();
            
            if (!response.ok) {
                throw new Error(result.error || 'Failed to process order');
            }
            
            resultElement.innerHTML = `
                <div class="success-message">
                    <h3>Order Submitted Successfully!</h3>
                    <p>User ID: ${formData.user_id}</p>
                    <p>Symbol: ${formData.symbol}</p>
                    <p>Type: ${formData.order_type.toUpperCase()}</p>
                    <p>Quantity: ${formData.quantity}</p>
                    <p>Price: $${formData.price.toFixed(2)}</p>
                    <button class="btn btn-primary view-portfolio-btn">View Updated Portfolio</button>
                </div>
            `;
            
            // Store the user ID for later use
            const userId = formData.user_id;
            
            // Add event listener AFTER the button is added to the DOM
            document.querySelector('.view-portfolio-btn').addEventListener('click', function() {
                console.log("View portfolio button clicked for user:", userId);
                showPortfolioDetail(userId);
            });
            
            form.reset();
            
        } catch (error) {
            resultElement.innerHTML = `
                <div class="error-message">
                    <p>${error.message}</p>
                </div>
            `;
        }
    }
    
    async function loadPortfolios() {
        const portfoliosListElement = document.getElementById('portfolios-list');
        portfoliosListElement.innerHTML = '<p class="loading">Loading portfolios...</p>';
        
        try {
            const response = await fetch(`${CONFIG.portfolioServiceUrl}/portfolios`);
            if (!response.ok) {
                throw new Error('Failed to load portfolios');
            }
            
            const portfolios = await response.json();
            
            if (Object.keys(portfolios).length === 0) {
                portfoliosListElement.innerHTML = `
                    <p class="message">No portfolios available yet. Create an order first.</p>
                `;
                return;
            }
            
            let portfolioHtml = '<ul class="portfolio-list">';
            
            for (const [userId, orders] of Object.entries(portfolios)) {
                portfolioHtml += `
                    <li>
                        <a href="#" class="portfolio-link" data-user-id="${userId}">
                            User ID: ${userId}
                            <span class="badge">${orders.length} orders</span>
                        </a>
                    </li>
                `;
            }
            
            portfolioHtml += '</ul>';
            portfoliosListElement.innerHTML = portfolioHtml;
            
            // Add click handlers to portfolio links
            document.querySelectorAll('.portfolio-link').forEach(link => {
                link.addEventListener('click', function(e) {
                    e.preventDefault();
                    const userId = this.getAttribute('data-user-id');
                    showPortfolioDetail(userId);
                });
            });
            
        } catch (error) {
            portfoliosListElement.innerHTML = `
                <div class="error-message">
                    <p>${error.message}</p>
                </div>
            `;
        }
    }
    
    async function loadPortfolioDetail(userId) {
        const detailElement = document.getElementById('portfolio-detail-content');
        detailElement.innerHTML = '<p class="loading">Loading portfolio details...</p>';
        
        try {
            const response = await fetch(`${CONFIG.portfolioServiceUrl}/portfolios/${userId}`);
            if (!response.ok) {
                throw new Error('Failed to load portfolio details');
            }
            
            const portfolio = await response.json();
            
            if (portfolio.length === 0) {
                detailElement.innerHTML = '<p class="message">No orders in this portfolio.</p>';
                return;
            }
            
            // Calculate total value
            let totalValue = 0;
            portfolio.forEach(order => {
                if (order.quantity && order.price) {
                    if (order.order_type.toLowerCase() === 'buy') {
                        totalValue += order.quantity * order.price;
                    } else if (order.order_type.toLowerCase() === 'sell') {
                        totalValue -= order.quantity * order.price;
                    }
                }
            });
            
            let html = `
                <div class="summary">
                    <p>User ID: <strong>${userId}</strong></p>
                    <p>Total Value: <strong>$${totalValue.toFixed(2)}</strong></p>
                    <p>Total Orders: <strong>${portfolio.length}</strong></p>
                </div>
                <table class="orders-table">
                    <thead>
                        <tr>
                            <th>Symbol</th>
                            <th>Type</th>
                            <th>Quantity</th>
                            <th>Price</th>
                            <th>Value</th>
                        </tr>
                    </thead>
                    <tbody>
            `;
            
            portfolio.forEach(order => {
                const orderValue = order.quantity * order.price;
                html += `
                    <tr class="${order.order_type === 'buy' ? 'order-buy' : 'order-sell'}">
                        <td>${order.symbol}</td>
                        <td>${order.order_type.toUpperCase()}</td>
                        <td>${order.quantity}</td>
                        <td>$${order.price.toFixed(2)}</td>
                        <td>$${orderValue.toFixed(2)}</td>
                    </tr>
                `;
            });
            
            html += `
                    </tbody>
                </table>
            `;
            
            detailElement.innerHTML = html;
            
        } catch (error) {
            detailElement.innerHTML = `
                <div class="error-message">
                    <p>${error.message}</p>
                </div>
            `;
        }
    }
});