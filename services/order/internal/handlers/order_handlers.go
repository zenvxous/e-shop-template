package handlers

import (
	"github.com/gofiber/fiber/v3"
	"github.com/google/uuid"

	"order/internal/domain"
)

type createOrderRequest struct {
	CartID uuid.UUID `json:"cart_id"`
}

type updateOrderStatusRequest struct {
	Status string `json:"status"`
}

func (h *Handlers) CreateOrder(c fiber.Ctx) error {
	var req createOrderRequest
	if err := c.Bind().JSON(&req); err != nil {
		return jsonError(c, fiber.StatusBadRequest, "invalid json")
	}
	if req.CartID == uuid.Nil {
		return jsonError(c, fiber.StatusBadRequest, "cart_id is required")
	}

	order, err := h.Order.CreateFromCart(c.Context(), req.CartID)
	if err != nil {
		return jsonError(c, fiber.StatusBadRequest, err.Error())
	}
	return c.Status(fiber.StatusCreated).JSON(order)
}

func (h *Handlers) GetOrder(c fiber.Ctx) error {
	orderID, err := uuid.Parse(c.Params("order_id"))
	if err != nil {
		return jsonError(c, fiber.StatusBadRequest, "invalid order_id")
	}

	order, err := h.Order.Get(c.Context(), orderID)
	if err != nil {
		return jsonError(c, fiber.StatusNotFound, err.Error())
	}
	return c.JSON(order)
}

func (h *Handlers) UpdateOrderStatus(c fiber.Ctx) error {
	orderID, err := uuid.Parse(c.Params("order_id"))
	if err != nil {
		return jsonError(c, fiber.StatusBadRequest, "invalid order_id")
	}
	var req updateOrderStatusRequest
	if err := c.Bind().JSON(&req); err != nil {
		return jsonError(c, fiber.StatusBadRequest, "invalid json")
	}

	var st domain.OrderStatus
	switch req.Status {
	case string(domain.OrderStatusPaid):
		st = domain.OrderStatusPaid
	case string(domain.OrderStatusCancelled):
		st = domain.OrderStatusCancelled
	default:
		return jsonError(c, fiber.StatusBadRequest, "status must be paid or cancelled")
	}

	order, err := h.Order.UpdateStatus(c.Context(), orderID, st)
	if err != nil {
		return jsonError(c, fiber.StatusBadRequest, err.Error())
	}
	return c.JSON(order)
}
