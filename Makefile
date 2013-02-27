export PROJECT := pore

#### target directories
export BUILD_DIR := assets
export TMP_DIR := tmp

### external programs and libraries
export SED := sed -r
export GIT := git
export NODE := node
export LESS := $(abspath $(TMP_DIR)/less.js)
export BOOTSTRAP := $(abspath $(TMP_DIR)/bootstrap)
export UGLIFY := $(abspath $(TMP_DIR)/UglifyJS)
export CSSO := $(abspath $(TMP_DIR)/csso)


### helper functions

# parses less imports from .less files (to check dependencies)
fn-grep-imports = $(foreach a,$(1),$(addprefix $(dir $(a)),$(shell $(SED) -n 's/^@import "([^"]+)".*/\1/p' $(a))))


### source file listings (when order is important; can use `find' otherwise)

export LESS_SOURCES := ui/$(PROJECT).less
export JS_SOURCES := \
	lib/jquery.form.js \
	$(BOOTSTRAP)/js/bootstrap-collapse.js \
	ui/$(PROJECT).js

### main targets

all: deps css-min js-min

deps: $(LESS) $(BOOTSTRAP) $(UGLIFY) $(CSSO)

libupdate: GITUP = $(GIT) pull --rebase
libupdate: deps
	@cd $(LESS) && $(GIT) fetch && $(GIT) checkout "v1.3.3"
	@cd $(BOOTSTRAP) && $(GIT) fetch && $(GIT) checkout "v2.3.0"
	@cd $(UGLIFY) && $(GITUP)
	@cd $(CSSO) && $(GITUP)

$(LESS):
	@$(GIT) clone -b "v1.3.3" --depth 1 https://github.com/cloudhead/less.js.git $@

$(BOOTSTRAP):
	@$(GIT) clone -b "v2.3.0" --depth 1 https://github.com/twitter/bootstrap.git $@

$(UGLIFY):
	@$(GIT) clone --depth 1 https://github.com/mishoo/UglifyJS.git $@

$(CSSO):
	@$(GIT) clone --depth 1 https://github.com/css/csso $@

css: $(BUILD_DIR)/css/$(PROJECT).css $(BUILD_DIR)/css/$(PROJECT)-responsive.css

css-min: $(BUILD_DIR)/css/$(PROJECT).min.css $(BUILD_DIR)/css/$(PROJECT)-responsive.min.css

# release css compilation rule
$(BUILD_DIR)/css/$(PROJECT).css: $(LESS_SOURCES:.less=.css) $(call fn-grep-imports,$(LESS_SOURCES))
	@cat $(LESS_SOURCES:.less=.css) > $@

$(BUILD_DIR)/css/$(PROJECT)-responsive.css: ui/$(PROJECT)-responsive.css $(call fn-grep-imports,$(ui/$(PROJECT)-responsive.less))
	@cp ui/$(PROJECT)-responsive.css $@

js: $(BUILD_DIR)/js/$(PROJECT).js

# release js compilation rule
$(BUILD_DIR)/js/$(PROJECT).js: $(JS_SOURCES) $(shell find $(PROJECT) -name '*.js')
	@cat $^ > $@

js-min: $(BUILD_DIR)/js/$(PROJECT).min.js

clean:
	@rm -f assets/js/$(PROJECT).js assets/js/$(PROJECT).min.js \
	       assets/css/$(PROJECT).css assets/css/$(PROJECT).min.css

.PHONY: all deps css css-min js js-min clean

.INTERMEDIATE: \
	$(LESS_SOURCES:.less=.css) \
	ui/$(PROJECT)-responsive.css \
	$(BOOTSTRAP)/less/bootstrap.css

.PRECIOUS: $(BUILD_DIR)/$(PROJECT).css


### generation rules

# LESS compilation
%.css: %.less
	@echo -n "Compiling $@ ... "
	@$(LESS)/bin/lessc $< > $@
	@echo "ok"

# CSS optimization
%.min.css: %.css
	@echo -n "Minifying $@ ... "
	@$(CSSO)/bin/csso $< $@
	@echo "ok"

# javascript optimization
%.min.js: %.js
	@echo -n "Minifying $@ ... "
	@$(UGLIFY)/bin/uglifyjs --max-line-len 120 -o $@ $<
	@echo "ok"
