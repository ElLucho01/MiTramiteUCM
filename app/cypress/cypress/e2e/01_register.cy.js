describe("Registro de usuario", () => {
  it("Debe registrar un usuario nuevo", () => {
    cy.visit("/");

    cy.get("#nombreReg").type("Juan Pérez");
    cy.get("#correoReg").type("juan@test.com");
    cy.get("#contrasenaReg").type("123456");

    cy.get("#registrarse").click();

    cy.url().should("include", "/home");
    cy.contains("Guía de recomendaciones básicas").should("be.visible");
  });
});

