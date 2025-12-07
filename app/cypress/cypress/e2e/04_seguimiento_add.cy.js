describe("Añadir beneficio a seguimiento", () => {
  beforeEach(() => {
    cy.visit("/");
    cy.get("#correoLog").type("juan@test.com");
    cy.get("#contrasenaLog").type("123456");
    cy.get("#loginButton").click();
  });

  it("Debe entrar al detalle del beneficio y agregar seguimiento", () => {
    cy.get(".benefit-item .detail-btn").first().click();

    cy.contains("Añadir a Seguimiento").click();

    cy.contains("Eliminar de Seguimiento").should("be.visible");
  });
});