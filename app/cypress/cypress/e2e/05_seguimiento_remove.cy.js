describe("Eliminar beneficio de seguimiento", () => {
  beforeEach(() => {
    cy.visit("/");
    cy.get("#correoLog").type("juan@test.com");
    cy.get("#contrasenaLog").type("123456");
    cy.get("#loginButton").click();

    // Asegurar que existe seguimiento
    cy.get(".benefit-item .detail-btn").last().click();
    cy.contains("Añadir a Seguimiento").click();
  });

  it("Debe eliminar un beneficio del seguimiento", () => {
    cy.contains("Eliminar de Seguimiento").click();

    cy.contains("Añadir a Seguimiento").should("be.visible");
  });
});
