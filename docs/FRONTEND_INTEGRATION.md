# Integración del Frontend con el Notification Service

## Descripción

Esta documentación explica cómo integrar el **Notification Service** con el frontend de SmartHydro para mostrar notificaciones en tiempo real.

## Arquitectura Frontend

```
┌─────────────────┐    ┌─────────────────────┐    ┌─────────────────┐
│   React/Vue     │    │  Notification       │    │   Django API    │
│   Frontend      │◄──►│  Service (FastAPI)  │◄──►│   (Business)    │
└─────────────────┘    └─────────────────────┘    └─────────────────┘
         │                       │
         ▼                       ▼
┌─────────────────┐    ┌─────────────────┐
│   WebSocket     │    │     Redis       │
│   Connection    │    │   (Pub/Sub)     │
└─────────────────┘    └─────────────────┘
```

## Componentes Frontend

### 1. Notification Service (JavaScript/TypeScript)

```typescript
// services/notificationService.ts
class NotificationService {
  private ws: WebSocket | null = null;
  private reconnectAttempts = 0;
  private maxReconnectAttempts = 5;
  private reconnectDelay = 1000;
  private listeners: Map<string, Function[]> = new Map();

  constructor(private baseUrl: string = "http://localhost:8006") {}

  // Conectar WebSocket
  async connect(token: string): Promise<void> {
    try {
      this.ws = new WebSocket(`ws://localhost:8006/ws/?token=${token}`);

      this.ws.onopen = () => {
        console.log("Conectado al servicio de notificaciones");
        this.reconnectAttempts = 0;
        this.emit("connected");
      };

      this.ws.onmessage = (event) => {
        try {
          const notification = JSON.parse(event.data);
          this.handleNotification(notification);
        } catch (error) {
          console.error("Error parsing notification:", error);
        }
      };

      this.ws.onclose = () => {
        console.log("Desconectado del servicio de notificaciones");
        this.emit("disconnected");
        this.reconnect(token);
      };

      this.ws.onerror = (error) => {
        console.error("Error en WebSocket:", error);
      };
    } catch (error) {
      console.error("Error conectando al servicio de notificaciones:", error);
    }
  }

  // Reconectar automáticamente
  private reconnect(token: string): void {
    if (this.reconnectAttempts < this.maxReconnectAttempts) {
      this.reconnectAttempts++;
      console.log(`Reconectando... Intento ${this.reconnectAttempts}`);

      setTimeout(() => {
        this.connect(token);
      }, this.reconnectDelay * this.reconnectAttempts);
    }
  }

  // Manejar notificación recibida
  private handleNotification(notification: any): void {
    console.log("Nueva notificación:", notification);

    // Emitir evento de notificación
    this.emit("notification", notification);

    // Mostrar notificación toast
    this.showToast(notification);
  }

  // Mostrar toast de notificación
  private showToast(notification: any): void {
    // Implementar según la librería de toast que uses
    // Ejemplo con react-toastify:
    if (window.toast) {
      window.toast.info(notification.message, {
        position: "top-right",
        autoClose: 5000,
        hideProgressBar: false,
        closeOnClick: true,
        pauseOnHover: true,
        draggable: true,
        progress: undefined,
      });
    }
  }

  // Event listeners
  on(event: string, callback: Function): void {
    if (!this.listeners.has(event)) {
      this.listeners.set(event, []);
    }
    this.listeners.get(event)!.push(callback);
  }

  off(event: string, callback: Function): void {
    const callbacks = this.listeners.get(event);
    if (callbacks) {
      const index = callbacks.indexOf(callback);
      if (index > -1) {
        callbacks.splice(index, 1);
      }
    }
  }

  private emit(event: string, data?: any): void {
    const callbacks = this.listeners.get(event);
    if (callbacks) {
      callbacks.forEach((callback) => callback(data));
    }
  }

  // Desconectar
  disconnect(): void {
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
  }

  // API REST methods
  async getNotifications(userId: number, params?: any): Promise<any> {
    const queryString = new URLSearchParams(params).toString();
    const response = await fetch(
      `${this.baseUrl}/notifications/user/${userId}?${queryString}`,
      {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`,
          "Content-Type": "application/json",
        },
      }
    );
    return response.json();
  }

  async markAsRead(notificationId: number): Promise<any> {
    const response = await fetch(
      `${this.baseUrl}/notifications/${notificationId}/mark-read`,
      {
        method: "POST",
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`,
          "Content-Type": "application/json",
        },
      }
    );
    return response.json();
  }

  async markAllAsRead(userId: number): Promise<any> {
    const response = await fetch(
      `${this.baseUrl}/notifications/user/${userId}/mark-all-read`,
      {
        method: "POST",
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`,
          "Content-Type": "application/json",
        },
      }
    );
    return response.json();
  }

  async getUnreadCount(userId: number): Promise<number> {
    const response = await fetch(
      `${this.baseUrl}/notifications/user/${userId}/unread-count`,
      {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`,
          "Content-Type": "application/json",
        },
      }
    );
    const data = await response.json();
    return data.unread_count;
  }

  async getUserPreferences(userId: number): Promise<any> {
    const response = await fetch(`${this.baseUrl}/preferences/user/${userId}`, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem("token")}`,
        "Content-Type": "application/json",
      },
    });
    return response.json();
  }

  async updateUserPreferences(userId: number, preferences: any): Promise<any> {
    const response = await fetch(`${this.baseUrl}/preferences/user/${userId}`, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${localStorage.getItem("token")}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify(preferences),
    });
    return response.json();
  }
}

export default NotificationService;
```

### 2. React Hook para Notificaciones

```typescript
// hooks/useNotifications.ts
import { useState, useEffect, useCallback } from "react";
import NotificationService from "../services/notificationService";

interface Notification {
  id: number;
  subject: string;
  message: string;
  priority: string;
  module: string;
  timestamp: string;
  metadata: any;
}

interface UseNotificationsReturn {
  notifications: Notification[];
  unreadCount: number;
  loading: boolean;
  error: string | null;
  markAsRead: (id: number) => Promise<void>;
  markAllAsRead: () => Promise<void>;
  refreshNotifications: () => Promise<void>;
}

export const useNotifications = (userId: number): UseNotificationsReturn => {
  const [notifications, setNotifications] = useState<Notification[]>([]);
  const [unreadCount, setUnreadCount] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const notificationService = new NotificationService();

  // Cargar notificaciones iniciales
  const loadNotifications = useCallback(async () => {
    try {
      setLoading(true);
      const [notificationsData, unreadCountData] = await Promise.all([
        notificationService.getNotifications(userId, { limit: 50 }),
        notificationService.getUnreadCount(userId),
      ]);

      setNotifications(notificationsData.notifications || []);
      setUnreadCount(unreadCountData);
      setError(null);
    } catch (err) {
      setError("Error cargando notificaciones");
      console.error("Error loading notifications:", err);
    } finally {
      setLoading(false);
    }
  }, [userId]);

  // Marcar como leída
  const markAsRead = useCallback(async (id: number) => {
    try {
      await notificationService.markAsRead(id);

      // Actualizar estado local
      setNotifications((prev) =>
        prev.map((notif) =>
          notif.id === id ? { ...notif, status: "read" } : notif
        )
      );

      // Actualizar conteo
      setUnreadCount((prev) => Math.max(0, prev - 1));
    } catch (err) {
      console.error("Error marking notification as read:", err);
    }
  }, []);

  // Marcar todas como leídas
  const markAllAsRead = useCallback(async () => {
    try {
      await notificationService.markAllAsRead(userId);

      // Actualizar estado local
      setNotifications((prev) =>
        prev.map((notif) => ({ ...notif, status: "read" }))
      );

      setUnreadCount(0);
    } catch (err) {
      console.error("Error marking all notifications as read:", err);
    }
  }, [userId]);

  // Refrescar notificaciones
  const refreshNotifications = useCallback(async () => {
    await loadNotifications();
  }, [loadNotifications]);

  // Efecto para cargar notificaciones iniciales
  useEffect(() => {
    loadNotifications();
  }, [loadNotifications]);

  // Efecto para conectar WebSocket
  useEffect(() => {
    const token = localStorage.getItem("token");
    if (token) {
      notificationService.connect(token);

      // Escuchar nuevas notificaciones
      notificationService.on(
        "notification",
        (newNotification: Notification) => {
          setNotifications((prev) => [newNotification, ...prev]);
          setUnreadCount((prev) => prev + 1);
        }
      );

      // Cleanup
      return () => {
        notificationService.disconnect();
      };
    }
  }, []);

  return {
    notifications,
    unreadCount,
    loading,
    error,
    markAsRead,
    markAllAsRead,
    refreshNotifications,
  };
};
```

### 3. Componente de Notificaciones (React)

```tsx
// components/NotificationCenter.tsx
import React, { useState } from "react";
import { useNotifications } from "../hooks/useNotifications";
import { formatDistanceToNow } from "date-fns";
import { es } from "date-fns/locale";

interface NotificationCenterProps {
  userId: number;
  isOpen: boolean;
  onClose: () => void;
}

const NotificationCenter: React.FC<NotificationCenterProps> = ({
  userId,
  isOpen,
  onClose,
}) => {
  const {
    notifications,
    unreadCount,
    loading,
    error,
    markAsRead,
    markAllAsRead,
    refreshNotifications,
  } = useNotifications(userId);

  const [activeTab, setActiveTab] = useState<"all" | "unread">("all");

  const filteredNotifications =
    activeTab === "unread"
      ? notifications.filter((n) => n.status === "sent")
      : notifications;

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case "urgent":
        return "text-red-600 bg-red-50";
      case "high":
        return "text-orange-600 bg-orange-50";
      case "medium":
        return "text-blue-600 bg-blue-50";
      case "low":
        return "text-gray-600 bg-gray-50";
      default:
        return "text-gray-600 bg-gray-50";
    }
  };

  const getModuleIcon = (module: string) => {
    switch (module) {
      case "payments":
        return "💰";
      case "banking":
        return "🏦";
      case "quotations":
        return "📋";
      case "support":
        return "🛠️";
      case "projects":
        return "📊";
      default:
        return "📢";
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 overflow-y-auto">
      <div className="flex items-center justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
        {/* Backdrop */}
        <div
          className="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity"
          onClick={onClose}
        />

        {/* Modal */}
        <div className="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full">
          {/* Header */}
          <div className="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
            <div className="flex items-center justify-between">
              <h3 className="text-lg leading-6 font-medium text-gray-900">
                Notificaciones
                {unreadCount > 0 && (
                  <span className="ml-2 inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-red-100 text-red-800">
                    {unreadCount}
                  </span>
                )}
              </h3>
              <div className="flex space-x-2">
                <button
                  onClick={refreshNotifications}
                  className="text-gray-400 hover:text-gray-600"
                  disabled={loading}
                >
                  🔄
                </button>
                <button
                  onClick={onClose}
                  className="text-gray-400 hover:text-gray-600"
                >
                  ✕
                </button>
              </div>
            </div>

            {/* Tabs */}
            <div className="flex space-x-4 mt-4 border-b">
              <button
                onClick={() => setActiveTab("all")}
                className={`pb-2 px-1 border-b-2 font-medium text-sm ${
                  activeTab === "all"
                    ? "border-blue-500 text-blue-600"
                    : "border-transparent text-gray-500 hover:text-gray-700"
                }`}
              >
                Todas ({notifications.length})
              </button>
              <button
                onClick={() => setActiveTab("unread")}
                className={`pb-2 px-1 border-b-2 font-medium text-sm ${
                  activeTab === "unread"
                    ? "border-blue-500 text-blue-600"
                    : "border-transparent text-gray-500 hover:text-gray-700"
                }`}
              >
                No leídas ({unreadCount})
              </button>
            </div>
          </div>

          {/* Content */}
          <div className="bg-white px-4 pb-4 sm:p-6 sm:pb-4">
            {loading ? (
              <div className="flex justify-center py-8">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
              </div>
            ) : error ? (
              <div className="text-center py-8 text-red-600">{error}</div>
            ) : filteredNotifications.length === 0 ? (
              <div className="text-center py-8 text-gray-500">
                No hay notificaciones
              </div>
            ) : (
              <div className="space-y-3 max-h-96 overflow-y-auto">
                {filteredNotifications.map((notification) => (
                  <div
                    key={notification.id}
                    className={`p-3 rounded-lg border cursor-pointer transition-colors ${
                      notification.status === "sent"
                        ? "bg-blue-50 border-blue-200"
                        : "bg-white border-gray-200"
                    }`}
                    onClick={() => markAsRead(notification.id)}
                  >
                    <div className="flex items-start space-x-3">
                      <div className="flex-shrink-0 text-xl">
                        {getModuleIcon(notification.module)}
                      </div>
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center justify-between">
                          <p className="text-sm font-medium text-gray-900">
                            {notification.subject}
                          </p>
                          <span
                            className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${getPriorityColor(
                              notification.priority
                            )}`}
                          >
                            {notification.priority}
                          </span>
                        </div>
                        <p className="text-sm text-gray-600 mt-1">
                          {notification.message}
                        </p>
                        <p className="text-xs text-gray-400 mt-2">
                          {formatDistanceToNow(
                            new Date(notification.timestamp),
                            {
                              addSuffix: true,
                              locale: es,
                            }
                          )}
                        </p>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Footer */}
          {notifications.length > 0 && (
            <div className="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse">
              <button
                type="button"
                onClick={markAllAsRead}
                className="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-blue-600 text-base font-medium text-white hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 sm:ml-3 sm:w-auto sm:text-sm"
              >
                Marcar todas como leídas
              </button>
              <button
                type="button"
                onClick={onClose}
                className="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 sm:mt-0 sm:ml-3 sm:w-auto sm:text-sm"
              >
                Cerrar
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default NotificationCenter;
```

### 4. Componente de Badge de Notificaciones

```tsx
// components/NotificationBadge.tsx
import React, { useState } from "react";
import { useNotifications } from "../hooks/useNotifications";
import NotificationCenter from "./NotificationCenter";

interface NotificationBadgeProps {
  userId: number;
}

const NotificationBadge: React.FC<NotificationBadgeProps> = ({ userId }) => {
  const { unreadCount } = useNotifications(userId);
  const [isOpen, setIsOpen] = useState(false);

  return (
    <>
      <button
        onClick={() => setIsOpen(true)}
        className="relative p-2 text-gray-600 hover:text-gray-900 focus:outline-none focus:ring-2 focus:ring-blue-500 rounded-md"
      >
        <svg
          className="h-6 w-6"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M15 17h5l-5 5v-5zM4.19 4.19C4.19 4.19 4.19 4.19 4.19 4.19zM4.19 4.19C4.19 4.19 4.19 4.19 4.19 4.19zM4.19 4.19C4.19 4.19 4.19 4.19 4.19 4.19zM4.19 4.19C4.19 4.19 4.19 4.19 4.19 4.19z"
          />
        </svg>

        {unreadCount > 0 && (
          <span className="absolute -top-1 -right-1 inline-flex items-center justify-center px-2 py-1 text-xs font-bold leading-none text-white transform translate-x-1/2 -translate-y-1/2 bg-red-600 rounded-full">
            {unreadCount > 99 ? "99+" : unreadCount}
          </span>
        )}
      </button>

      <NotificationCenter
        userId={userId}
        isOpen={isOpen}
        onClose={() => setIsOpen(false)}
      />
    </>
  );
};

export default NotificationBadge;
```

### 5. Integración en el Layout Principal

```tsx
// components/Layout.tsx
import React from "react";
import NotificationBadge from "./NotificationBadge";

interface LayoutProps {
  children: React.ReactNode;
  userId: number;
}

const Layout: React.FC<LayoutProps> = ({ children, userId }) => {
  return (
    <div className="min-h-screen bg-gray-100">
      {/* Header */}
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <div className="flex items-center">
              <h1 className="text-2xl font-bold text-gray-900">SmartHydro</h1>
            </div>

            <div className="flex items-center space-x-4">
              {/* Otros elementos del header */}
              <NotificationBadge userId={userId} />
            </div>
          </div>
        </div>
      </header>

      {/* Main content */}
      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">{children}</main>
    </div>
  );
};

export default Layout;
```

## Configuración del Proyecto

### 1. Variables de Entorno

```bash
# .env
REACT_APP_NOTIFICATION_SERVICE_URL=http://localhost:8006
REACT_APP_WS_URL=ws://localhost:8006
```

### 2. Configuración de Toast (Opcional)

```bash
# Instalar react-toastify
npm install react-toastify
```

```tsx
// App.tsx
import { ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

function App() {
  return (
    <div>
      {/* Tu aplicación */}
      <ToastContainer
        position="top-right"
        autoClose={5000}
        hideProgressBar={false}
        newestOnTop={false}
        closeOnClick
        rtl={false}
        pauseOnFocusLoss
        draggable
        pauseOnHover
      />
    </div>
  );
}
```

## Uso en Componentes

```tsx
// Ejemplo de uso en un componente
import React from "react";
import { useNotifications } from "../hooks/useNotifications";

const Dashboard: React.FC = () => {
  const { unreadCount } = useNotifications(1); // userId = 1

  return (
    <div>
      <h1>Dashboard</h1>
      <p>Tienes {unreadCount} notificaciones no leídas</p>
      {/* Resto del contenido */}
    </div>
  );
};
```

## Consideraciones de Rendimiento

1. **Lazy Loading**: Cargar notificaciones solo cuando sea necesario
2. **Paginación**: Implementar paginación para listas largas
3. **Debouncing**: Evitar múltiples llamadas simultáneas
4. **Caching**: Cachear notificaciones en localStorage
5. **WebSocket**: Reconexión automática y manejo de errores

## Testing

```typescript
// tests/notificationService.test.ts
import NotificationService from "../services/notificationService";

describe("NotificationService", () => {
  let service: NotificationService;

  beforeEach(() => {
    service = new NotificationService();
  });

  test("should connect to WebSocket", async () => {
    const token = "test-token";
    await service.connect(token);
    // Verificar conexión
  });

  test("should handle notifications", () => {
    const mockNotification = {
      id: 1,
      subject: "Test",
      message: "Test message",
    };

    const callback = jest.fn();
    service.on("notification", callback);

    // Simular mensaje WebSocket
    service["handleNotification"](mockNotification);

    expect(callback).toHaveBeenCalledWith(mockNotification);
  });
});
```

Esta integración proporciona una experiencia completa de notificaciones en tiempo real para el frontend de SmartHydro, manteniendo la consistencia con la arquitectura de microservicios.
