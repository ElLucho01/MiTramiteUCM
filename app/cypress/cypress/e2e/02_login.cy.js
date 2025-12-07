describe("Login de usuario", () => {
  it("Debe iniciar sesión correctamente", () => {
    cy.visit("/");

    cy.get("#correoLog").type("juan@test.com");
    cy.get("#contrasenaLog").type("123456");

    cy.get("#loginButton").click();

    cy.url().should("include", "/home");
    cy.contains("Guía de recomendaciones básicas").should("be.visible");
  });

  it("Debe mostrar error con credenciales incorrectas", () => {
    cy.visit("/");

    cy.get("#correoLog").type("fake@test.com");
    cy.get("#contrasenaLog").type("wrong");

    cy.get("#loginButton").click();

    cy.contains("Correo o contraseña incorrectos").should("be.visible");
  });
});
