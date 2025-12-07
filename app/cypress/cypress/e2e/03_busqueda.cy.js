describe("Buscador de beneficios", () => {
  beforeEach(() => {
    cy.visit("/");
    cy.get("#correoLog").type("juan@test.com");
    cy.get("#contrasenaLog").type("123456");
    cy.get("#loginButton").click();
  });

  it("Debe buscar un beneficio y mostrar resultados", () => {
    cy.get("#busquedaBeneficios").type("beca");

    cy.get("#resultadosBusqueda")
      .should("be.visible")
      .find(".resultado-item")
      .should("have.length.at.least", 1);
  });

  it("Debe navegar al beneficio seleccionado", () => {
    cy.get("#busquedaBeneficios").type("beca");

    cy.get(".resultado-item").first().click();

    cy.url().should("include", "/beneficio/");
    cy.get(".benefit-title").should("be.visible");
  });
});
