/* ══════════════════════════════════════════════
   FERI — Real-Time Order Notification Service
   Channels: Telegram Bot Push & WhatsApp Dispatch
   ══════════════════════════════════════════════ */

const NotificationService = (() => {
  const STORAGE_KEY = 'feri_notification_settings';

  // Default configuration pre-wired with verified credentials
  const defaultConfig = {
    telegramEnabled: true,
    telegramBotToken: '8187315790:AAEbEDDjYUq0PeJTTmjO4ZjLWv9RGCdNtgo',
    telegramChatId: '7837003396',
    whatsappPhone: '917767899764',
    whatsappEnabled: true
  };

  function getConfig() {
    try {
      const saved = localStorage.getItem(STORAGE_KEY);
      if (saved) return { ...defaultConfig, ...JSON.parse(saved) };
    } catch (e) {
      console.warn('Error reading notification settings:', e);
    }
    return { ...defaultConfig };
  }

  function saveConfig(cfg) {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(cfg));
      return true;
    } catch (e) {
      console.error('Error saving notification settings:', e);
      return false;
    }
  }

  // Format order into a clean, professional text receipt
  function formatOrderText(order) {
    const d = new Date(order.date || Date.now());
    const dateStr = d.toLocaleDateString('en-IN', {
      day: 'numeric',
      month: 'short',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });

    const storeName = 'New Shree Kirana';
    const customer = (order.address && order.address.name) ? order.address.name : 'Rajesh Kumar';
    const phone = (order.address && order.address.phone) ? order.address.phone : '+91 98765 43210';
    const addressStr = order.address
      ? `${order.address.addressLine || ''}, ${order.address.city || 'Mumbai'} - ${order.address.pincode || '400053'}`
      : 'Flat 402, Shanti Heights, Andheri West, Mumbai';

    let itemsText = '';
    if (order.items && order.items.length) {
      itemsText = order.items.map((it, idx) => {
        const itemPrice = (it.priceAtPurchase || it.price || 0) * (it.qty || 1);
        return `${idx + 1}. ${it.name} (x${it.qty}) — ₹${itemPrice.toLocaleString('en-IN')}`;
      }).join('\n');
    } else {
      itemsText = '• Items processed in cart';
    }

    const grandTotal = (order.totals && order.totals.grandTotal)
      ? '₹' + order.totals.grandTotal.toLocaleString('en-IN')
      : '₹4,560';

    const itemCount = order.items ? order.items.length : 0;
    const payment = order.paymentMethod || 'Credit';

    return `🛍️ *NEW ORDER RECEIVED! — FERI*
━━━━━━━━━━━━━━━━━━━━
📦 *Order ID:* #${order.id || 'ORD12345'}
📅 *Time:* ${dateStr}
🏪 *Store:* ${storeName}
👤 *Customer:* ${customer} (${phone})
📍 *Address:* ${addressStr}
━━━━━━━━━━━━━━━━━━━━
🛒 *ITEMS ORDERED (${itemCount}):*
${itemsText}
━━━━━━━━━━━━━━━━━━━━
💵 *Grand Total:* *${grandTotal}*
💳 *Payment:* ${payment}
🚚 *Expected Delivery:* ${order.expectedDelivery || 'Within 24-48 hours'}
━━━━━━━━━━━━━━━━━━━━
⚡ _Manage order in Feri App_`;
  }

  // Send real Telegram push alert via Bot API
  async function sendTelegramAlert(order) {
    const config = getConfig();
    if (!config.telegramEnabled) {
      return { skipped: true, reason: 'Telegram notifications disabled in settings' };
    }

    if (!config.telegramBotToken || !config.telegramChatId) {
      console.info('[NotificationService] Telegram Token or Chat ID not yet set in Account > Notification Settings');
      return {
        configured: false,
        error: 'Telegram Bot Token or Chat ID not configured. Please add them in Account Settings.'
      };
    }

    const message = formatOrderText(order);
    const url = `https://api.telegram.org/bot${encodeURIComponent(config.telegramBotToken)}/sendMessage`;

    try {
      const response = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          chat_id: config.telegramChatId,
          text: message,
          parse_mode: 'Markdown'
        })
      });

      const data = await response.json();
      if (data.ok) {
        console.log('[NotificationService] Telegram order alert sent successfully:', data);
        return { success: true, data };
      } else {
        console.warn('[NotificationService] Telegram API error:', data);
        return { success: false, error: data.description || 'Telegram API error' };
      }
    } catch (err) {
      console.error('[NotificationService] Network error sending Telegram alert:', err);
      return { success: false, error: err.message };
    }
  }

  // Get WhatsApp share URL (1-tap pre-filled receipt)
  function getWhatsAppUrl(order, customPhone) {
    const config = getConfig();
    const phone = customPhone || config.whatsappPhone || '';
    const cleanPhone = phone.replace(/[^0-9]/g, '');
    const text = formatOrderText(order);

    if (cleanPhone) {
      return `https://wa.me/${cleanPhone}?text=${encodeURIComponent(text)}`;
    }
    return `https://api.whatsapp.com/send?text=${encodeURIComponent(text)}`;
  }

  // Dispatch all enabled order notifications
  async function sendOrderNotification(order) {
    console.log('[NotificationService] Triggering order notification for order:', order.id);

    // 1. Telegram background alert
    const telegramPromise = sendTelegramAlert(order);

    // 2. Play audible confirmation tone
    if (typeof playSound === 'function') {
      try { playSound('notification'); } catch (e) {}
    }

    const telegramResult = await telegramPromise;
    return {
      orderId: order.id,
      telegram: telegramResult,
      whatsappUrl: getWhatsAppUrl(order)
    };
  }

  // Send a live test alert to verify setup
  async function sendTestAlert(channel = 'telegram') {
    const sampleOrder = {
      id: 'TEST' + Math.floor(1000 + Math.random() * 9000),
      date: new Date().toISOString(),
      items: [
        { name: 'Fortune Sunlite Refined Oil 1L', qty: 2, priceAtPurchase: 135 },
        { name: 'Aashirvaad Atta 5kg', qty: 1, priceAtPurchase: 249 },
        { name: 'Tata Tea Premium 1kg', qty: 1, priceAtPurchase: 435 }
      ],
      totals: { grandTotal: 954 },
      status: 'Test Notification',
      paymentMethod: 'Credit',
      expectedDelivery: 'Tomorrow, 5:00 PM',
      address: {
        name: 'Rajesh Kumar (Store Admin)',
        phone: '+91 98765 43210',
        addressLine: 'New Shree Kirana Store, Link Road',
        city: 'Mumbai',
        pincode: '400053'
      }
    };

    if (channel === 'telegram') {
      return await sendTelegramAlert(sampleOrder);
    } else if (channel === 'whatsapp') {
      const url = getWhatsAppUrl(sampleOrder);
      window.open(url, '_blank');
      return { success: true, opened: true };
    }
  }

  return {
    getConfig,
    saveConfig,
    formatOrderText,
    sendTelegramAlert,
    getWhatsAppUrl,
    sendOrderNotification,
    sendTestAlert
  };
})();

if (typeof window !== 'undefined') {
  window.NotificationService = NotificationService;
}
