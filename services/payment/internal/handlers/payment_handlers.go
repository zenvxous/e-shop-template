package handlers

import (
	"github.com/gofiber/fiber/v3"
	"github.com/google/uuid"
	"github.com/shopspring/decimal"
)

type createSessionRequest struct {
	OrderID   uuid.UUID       `json:"order_id"`
	Amount    decimal.Decimal `json:"amount"`
	Currency  string          `json:"currency"`
}

func (h *Handlers) CreateSession(c fiber.Ctx) error {
	var req createSessionRequest
	if err := c.Bind().JSON(&req); err != nil {
		return jsonError(c, fiber.StatusBadRequest, "invalid json")
	}
	if req.OrderID == uuid.Nil {
		return jsonError(c, fiber.StatusBadRequest, "order_id is required")
	}
	if req.Amount.IsNegative() {
		return jsonError(c, fiber.StatusBadRequest, "amount must be >= 0")
	}
	if req.Currency == "" {
		return jsonError(c, fiber.StatusBadRequest, "currency is required")
	}

	session, err := h.Payment.CreateSession(c.Context(), req.OrderID, req.Amount, req.Currency)
	if err != nil {
		return jsonError(c, fiber.StatusInternalServerError, err.Error())
	}
	return c.Status(fiber.StatusCreated).JSON(session)
}

func (h *Handlers) GetSession(c fiber.Ctx) error {
	id, err := uuid.Parse(c.Params("id"))
	if err != nil {
		return jsonError(c, fiber.StatusBadRequest, "invalid id")
	}
	session, err := h.Payment.GetSession(c.Context(), id)
	if err != nil {
		return jsonError(c, fiber.StatusNotFound, err.Error())
	}
	return c.JSON(session)
}

func (h *Handlers) ConfirmSession(c fiber.Ctx) error {
	id, err := uuid.Parse(c.Params("id"))
	if err != nil {
		return jsonError(c, fiber.StatusBadRequest, "invalid id")
	}
	session, err := h.Payment.ConfirmSession(c.Context(), id)
	if err != nil {
		return jsonError(c, fiber.StatusInternalServerError, err.Error())
	}
	return c.JSON(session)
}
