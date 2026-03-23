package handlers

import (
	"github.com/gofiber/fiber/v3"
	"github.com/google/uuid"
	"github.com/shopspring/decimal"
)

type createCartRequest struct {
	UserID uuid.UUID `json:"user_id"`
}

type addCartItemRequest struct {
	ProductID uuid.UUID       `json:"product_id"`
	Quantity  int             `json:"quantity"`
	Price     decimal.Decimal `json:"price"`
}

type updateCartItemRequest struct {
	Quantity int `json:"quantity"`
}

func (h *Handlers) CreateCart(c fiber.Ctx) error {
	var req createCartRequest
	if err := c.Bind().JSON(&req); err != nil {
		return jsonError(c, fiber.StatusBadRequest, "invalid json")
	}
	if req.UserID == uuid.Nil {
		return jsonError(c, fiber.StatusBadRequest, "user_id is required")
	}

	cart, err := h.Cart.CreateCart(c.Context(), req.UserID)
	if err != nil {
		return jsonError(c, fiber.StatusInternalServerError, err.Error())
	}
	return c.Status(fiber.StatusCreated).JSON(cart)
}

func (h *Handlers) AddCartItem(c fiber.Ctx) error {
	cartID, err := uuid.Parse(c.Params("cart_id"))
	if err != nil {
		return jsonError(c, fiber.StatusBadRequest, "invalid cart_id")
	}
	var req addCartItemRequest
	if err := c.Bind().JSON(&req); err != nil {
		return jsonError(c, fiber.StatusBadRequest, "invalid json")
	}
	if req.ProductID == uuid.Nil {
		return jsonError(c, fiber.StatusBadRequest, "product_id is required")
	}
	if req.Price.IsNegative() {
		return jsonError(c, fiber.StatusBadRequest, "price must be >= 0")
	}

	cart, err := h.Cart.AddItem(c.Context(), cartID, req.ProductID, req.Quantity, req.Price)
	if err != nil {
		return jsonError(c, fiber.StatusBadRequest, err.Error())
	}
	return c.JSON(cart)
}

func (h *Handlers) UpdateCartItem(c fiber.Ctx) error {
	cartID, err := uuid.Parse(c.Params("cart_id"))
	if err != nil {
		return jsonError(c, fiber.StatusBadRequest, "invalid cart_id")
	}
	itemID, err := uuid.Parse(c.Params("item_id"))
	if err != nil {
		return jsonError(c, fiber.StatusBadRequest, "invalid item_id")
	}
	var req updateCartItemRequest
	if err := c.Bind().JSON(&req); err != nil {
		return jsonError(c, fiber.StatusBadRequest, "invalid json")
	}

	cart, err := h.Cart.UpdateItemQuantity(c.Context(), cartID, itemID, req.Quantity)
	if err != nil {
		return jsonError(c, fiber.StatusBadRequest, err.Error())
	}
	return c.JSON(cart)
}

func (h *Handlers) DeleteCartItem(c fiber.Ctx) error {
	cartID, err := uuid.Parse(c.Params("cart_id"))
	if err != nil {
		return jsonError(c, fiber.StatusBadRequest, "invalid cart_id")
	}
	itemID, err := uuid.Parse(c.Params("item_id"))
	if err != nil {
		return jsonError(c, fiber.StatusBadRequest, "invalid item_id")
	}
	if err := h.Cart.DeleteItem(c.Context(), cartID, itemID); err != nil {
		return jsonError(c, fiber.StatusInternalServerError, err.Error())
	}
	return c.SendStatus(fiber.StatusNoContent)
}
